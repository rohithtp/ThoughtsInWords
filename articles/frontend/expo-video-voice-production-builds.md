# Building Production-Grade Video and Voice Systems with Expo Development Builds

**Date:** July 17, 2026

## Introduction

For a long time, the standard playbook for building real-time audio/video streaming or complex voice-to-text applications in React Native was straightforward: **eject to the React Native CLI immediately**. The limitations of pre-baked environments like Expo Go — which restrict you to a fixed set of native APIs — made it impossible to integrate custom WebRTC engines, native VoIP frameworks (like iOS CallKit and Android ConnectionService), or low-latency background audio protocols.

However, the architecture landscape has shifted dramatically. By leveraging **Expo Development Builds (`expo-dev-client`)** and **Continuous Native Generation (CNG)**, teams can build highly sophisticated, enterprise-scale video and voice systems without losing the velocity of the Expo ecosystem.

This article is an architectural deep dive into constructing production-ready communication platforms using custom Expo runtimes.

---

## The Core Architecture: Bridging JS and Native Audio/Video

Real-time video and voice systems require deep, non-blocking hooks into the underlying mobile OS layers: hardware camera/microphone access, hardware codecs, system-level audio session routing, and persistence when the app is backgrounded or killed.

In a modern Expo application, this is achieved by constructing a **Custom Development Client**. Instead of relying on a generic sandbox, you compile a custom binary that includes your specific native dependencies, while retaining web-like JavaScript hot-reloading over the air during development.

```
┌────────────────────────────────────────────────────────┐
│                   JavaScript Application Layer         │
│         (React, Expo Router, App State / Context)      │
└───────────────────────────┬────────────────────────────┘
                            │ (JSI / TurboModules)
┌───────────────────────────▼────────────────────────────┐
│              Expo Development Client Build             │
│  ┌───────────────────────┬──────────────────────────┐  │
│  │   WebRTC / Video SDK  │  System VoIP Frameworks  │  │
│  │   (LiveKit / Agora)   │  (CallKit / Connection)  │  │
│  └───────────────────────┴──────────────────────────┘  │
└───────────────────────────┬────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────┐
│                    iOS / Android OS                    │
└────────────────────────────────────────────────────────┘
```

### Why Legacy Solutions Fail on the New Architecture

If your system includes ancillary voice features like live transcription or real-time voice-to-text, legacy libraries (such as `@react-native-voice/voice`) often fail silently when running in React Native's modern New Architecture or bridgeless mode. They depend on the legacy serialized message queue — the old asynchronous bridge that batched native-to-JS calls through JSON serialization.

Production-grade voice and video systems must target **TurboModules** or **Expo Modules** that interface directly via the JavaScript Interface (JSI), ensuring that high-frequency audio callbacks or stream status updates do not block the UI thread. JSI allows synchronous, zero-copy calls between JavaScript and native code, which is essential when audio buffers must be handed off every 10–20 milliseconds without introducing jank.

---

## Infrastructure Setup and Continuous Native Generation

To keep the project maintainable, avoid manually tweaking files inside `/ios` or `/android` directories. Instead, treat the native directories as ephemeral build artifacts generated entirely by **Config Plugins**.

### Step 1: Initialize the Core Dev Client

Install the required development client package to transform your project into a custom engine:

```bash
npx expo install expo-dev-client
```

This single package replaces the Expo Go launcher with a custom-compiled development client. Your app still connects to the Expo Dev Server for Fast Refresh, but the binary now includes whatever native modules you install.

### Step 2: Configure System Permissions

Real-time communication applications require strict background capabilities and explicit hardware permissions. Configure your `app.json` so that Expo's prebuild engine generates the correct `Info.plist` and `AndroidManifest.xml` entries automatically:

```json
{
  "expo": {
    "name": "EnterpriseVC",
    "slug": "enterprise-vc",
    "ios": {
      "bundleIdentifier": "com.enterprise.vc",
      "infoPlist": {
        "NSCameraUsageDescription": "This app requires camera access for live video calls.",
        "NSMicrophoneUsageDescription": "This app requires microphone access for real-time audio streaming.",
        "UIBackgroundModes": ["audio", "voip", "fetch", "remote-notification"]
      }
    },
    "android": {
      "package": "com.enterprise.vc",
      "permissions": [
        "CAMERA",
        "RECORD_AUDIO",
        "MODIFY_AUDIO_SETTINGS",
        "BLUETOOTH",
        "ACCESS_NETWORK_STATE"
      ]
    },
    "plugins": [
      [
        "expo-media-library",
        {
          "savePhotosPermission": "Grant permission to save screenshots of calls."
        }
      ]
    ]
  }
}
```

The key entry is `UIBackgroundModes` on iOS. Without `"voip"` registered in this array, iOS will suspend your app's audio session when the user switches to another application. The `"audio"` mode allows background audio playback, and `"remote-notification"` enables push-triggered wake-ups for incoming call notifications.

On Android, `MODIFY_AUDIO_SETTINGS` is critical — it allows your app to switch between speakerphone, earpiece, and Bluetooth audio routes, which is non-negotiable for a production call interface.

---

## Selecting the Core Infrastructure

When building production-grade video and voice systems, rolling your own raw WebRTC infrastructure via `react-native-webrtc` gives you maximum flexibility but requires enormous engineering overhead for global SFU (Selective Forwarding Unit) routing, TURN server management, and bandwidth adaptation.

For enterprise-scale platforms, leveraging optimized native wrappers via Expo Config Plugins is highly recommended.

| Provider | Best For | Native Architecture | Expo Integration |
| :--- | :--- | :--- | :--- |
| **LiveKit** | Open-source self-hosting, sub-100ms latency, high scale | Native Swift/Kotlin SDKs wrapped for React Native | Verified Config Plugin |
| **Agora** | Global scale, out-of-the-box PSTN (telephony) bridging | C++ core with high-performance native bridges | Custom Config Plugin |
| **Stream Video** | Fast UI implementation with rich call diagnostics | Custom React Native SDK with JSI optimizations | Pre-configured Expo support |

### LiveKit

LiveKit is fully open-source (Apache 2.0) and can be self-hosted. Its React Native SDK wraps native Swift and Kotlin SDKs, meaning the actual WebRTC session management, codec negotiation, and SFU communication happen in native code. The JavaScript layer handles UI state and event callbacks.

LiveKit provides a verified Expo Config Plugin, which means `npx expo prebuild` automatically configures the native projects with the correct build settings, permissions, and linking.

### Agora

Agora's core engine is written in C++ and compiled for each platform. It handles codec selection, bandwidth estimation, and packet loss concealment at the native layer. Agora's global edge network of SFU servers means you do not need to deploy your own media infrastructure.

Agora does not ship a first-party Expo Config Plugin, so you will need to write a custom plugin or use a community-maintained one. This is straightforward — a config plugin is a JavaScript function that modifies the generated `ios/` and `android/` project files during `npx expo prebuild`.

### Stream Video

Stream provides a React Native SDK with pre-built UI components (call controls, participant grids, screen sharing views) and JSI-optimized native bindings. It is the fastest path to a working video call UI, at the cost of less architectural control.

---

## Production-Grade Implementation

Here is a structural example of initializing a robust, real-time video room manager using an SFU architecture within an Expo Development Build environment. It handles audio tracking, camera management, and graceful cleanup to prevent native thread memory leaks.

```tsx
import React, { useEffect, useState } from 'react';
import { StyleSheet, View, Text, ActivityIndicator, Pressable } from 'react-native';
import { Room, RoomEvent, VideoPresets } from '@livekit/components-react-native';

interface CallScreenProps {
  roomUrl: string;
  token: string;
  onCallLeave: () => void;
}

export const ProductionCallScreen = ({
  roomUrl,
  token,
  onCallLeave,
}: CallScreenProps) => {
  const [room, setRoom] = useState<Room | null>(null);
  const [isConnecting, setIsConnecting] = useState(true);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  useEffect(() => {
    // 1. Initialize the native WebRTC room instance
    const activeRoom = new Room({
      adaptiveStream: true, // Dynamically scales video resolution based on view size
      dynacast: true,       // Pauses publishing video layers with no subscribers
      videoCaptureDefaults: {
        resolution: VideoPresets.h720.resolution,
      },
    });

    // 2. Attach production event listeners
    activeRoom.on(RoomEvent.Connected, () => {
      setIsConnecting(false);
    });

    activeRoom.on(RoomEvent.ConnectionQualityChanged, (quality, participant) => {
      console.warn(
        `Participant ${participant.identity} connection quality: ${quality}`
      );
    });

    activeRoom.on(RoomEvent.Disconnected, () => {
      onCallLeave();
    });

    activeRoom.on(RoomEvent.FailedToConnect, (error) => {
      setErrorMessage(error.message);
      setIsConnecting(false);
    });

    // 3. Connect to the signaling server
    activeRoom
      .connect(roomUrl, token)
      .then(() => {
        activeRoom.localParticipant.setCameraEnabled(true);
        activeRoom.localParticipant.setMicrophoneEnabled(true);
        setRoom(activeRoom);
      })
      .catch((err) => {
        setErrorMessage(
          err instanceof Error ? err.message : 'Unknown connection error'
        );
        setIsConnecting(false);
      });

    // 4. Strict cleanup to release hardware camera and microphone locks
    return () => {
      activeRoom.disconnect();
    };
  }, [roomUrl, token]);

  if (isConnecting) {
    return (
      <View style={styles.centered}>
        <ActivityIndicator size="large" color="#007AFF" />
        <Text style={styles.statusText}>
          Negotiating secure peer connections...
        </Text>
      </View>
    );
  }

  if (errorMessage) {
    return (
      <View style={styles.centered}>
        <Text style={styles.errorText}>
          Connection Failure: {errorMessage}
        </Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <Text style={styles.activeCallText}>
        Active Video Session Connected
      </Text>

      <View style={styles.controlBar}>
        <Pressable
          style={styles.hangUpButton}
          onPress={() => room?.disconnect()}
        >
          <Text style={styles.buttonText}>Disconnect</Text>
        </Pressable>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#111',
    justifyContent: 'space-between',
  },
  centered: {
    flex: 1,
    backgroundColor: '#111',
    justifyContent: 'center',
    alignItems: 'center',
    padding: 24,
  },
  statusText: {
    color: '#aaa',
    marginTop: 12,
    fontSize: 16,
    textAlign: 'center',
  },
  errorText: {
    color: '#FF3B30',
    fontSize: 16,
    fontWeight: '600',
    textAlign: 'center',
  },
  activeCallText: {
    color: '#fff',
    fontSize: 18,
    textAlign: 'center',
    marginTop: 60,
  },
  controlBar: {
    paddingBottom: 40,
    alignItems: 'center',
  },
  hangUpButton: {
    backgroundColor: '#FF3B30',
    paddingVertical: 14,
    paddingHorizontal: 48,
    borderRadius: 28,
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
});
```

### Key Architectural Decisions in This Code

- **`adaptiveStream: true`** — The SDK monitors the rendered size of each remote participant's video view and automatically requests only the resolution needed. A thumbnail-sized participant tile receives 180p instead of 720p, saving bandwidth.
- **`dynacast: true`** — When no remote participant is subscribing to your video (e.g., you are the only person in the room), the SDK stops encoding and transmitting video entirely. This saves CPU, battery, and bandwidth.
- **Strict cleanup in the `useEffect` return** — Calling `activeRoom.disconnect()` in the cleanup function is critical. Without it, the native camera and microphone hardware locks persist even after the React component unmounts, preventing other apps (or even your own app on re-navigation) from accessing the hardware.

---

## Critical Production Architecture Checklists

When taking an Expo-based voice/video system to scale, the app will live or die based on handling OS interrupts and network transitions. Ensure your implementation accounts for the following edge cases.

### Audio Session Routing (The Telecom Paradigm)

Mobile operating systems prioritize phone calls above all else. You must integrate a native audio session manager plugin to react to interrupts.

**The Problem:** An incoming GSM cellular call will strip audio hardware control away from your application. On iOS, the system posts an `AVAudioSession.interruptionNotification`. On Android, the `AudioManager` signals an audio focus loss.

**The Mitigation Strategy:** Listen to native system notifications. When a `beginInterrupt` event occurs:

1. Pause your local WebRTC stream.
2. Mute data publishing to avoid sending silence frames.
3. Display a "Call Paused by System" overlay to the user.
4. On `endInterrupt`, re-negotiate the audio stream state — request audio focus, reconfigure the audio session category, and resume publishing.

Failing to handle this correctly results in one-way audio (the remote participant can hear you, but you cannot hear them) or complete audio loss that persists until the app is force-killed.

### Strict Network State Transitions

Mobile devices constantly bounce between Wi-Fi routers and cellular towers (LTE/5G). Each transition triggers an ICE (Interactive Connectivity Establishment) renegotiation.

**Implementation:** Leverage `expo-network` or your WebRTC engine's connection quality hooks to handle ICE restart tracking. If the network drop lasts less than 15 seconds, trigger a silent `reconnect()` loop instead of completely tearing down the functional UI layout. Most production WebRTC SDKs (LiveKit, Agora) handle ICE restarts automatically, but you must ensure your UI state machine does not prematurely show a "Call Ended" screen during a brief network transition.

### Background Execution and Push Notifications

When the app is backgrounded or the device is locked:

- **iOS:** The `voip` background mode keeps a persistent connection alive. For incoming calls, use **PushKit** (VoIP push notifications) which wake your app even if it has been terminated. This is mandatory for production call apps — standard APNs notifications do not wake terminated apps reliably.
- **Android:** Use a **Foreground Service** with the `microphone` and `camera` foreground service types (required since Android 14). This keeps the audio/video streams active when the user navigates away. Display an ongoing notification with call controls (mute, hang up).

### Build Pipelines with EAS

Because real-time communication modules alter native dependency graphs (`Gradle`, `CocoaPods`, native C++ headers), configure distinct build profiles inside `eas.json`:

```json
{
  "build": {
    "development": {
      "developmentClient": true,
      "distribution": "internal",
      "ios": {
        "simulator": true
      }
    },
    "production": {
      "developmentClient": false,
      "distribution": "store"
    }
  }
}
```

Run `eas build --profile development` anytime a new native communication module or configuration parameter is added. This ensures your local dev team is running a perfectly matched environment. The `"distribution": "internal"` setting allows you to distribute development builds directly to team members via QR code or link, without going through TestFlight or Google Play internal testing.

---

## Conclusion

The era of "eject from Expo to build serious communication apps" is over. Expo Development Builds with CNG provide the same native access as a bare React Native project — hardware camera/microphone control, system VoIP frameworks, native WebRTC engines — while preserving the developer experience advantages that make Expo compelling: Fast Refresh, config plugins, EAS Build, and OTA JavaScript updates.

The key architectural insight is that your native layer (WebRTC SDK, audio session management, VoIP push handling) is configured declaratively through config plugins and compiled into a custom binary, while your application logic and UI remain in JavaScript with instant hot-reload cycles. You get the best of both worlds without maintaining manual native project files.
