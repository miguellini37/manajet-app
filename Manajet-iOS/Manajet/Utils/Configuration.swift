//
//  Configuration.swift
//  Manajet
//
//  Environment configuration for switching between dev and production
//

import Foundation

enum Environment {
    case development
    case production

    var baseURL: String {
        switch self {
        case .development:
            // Local development - update with your Mac's IP address
            // Find it: System Settings → Network → Details → TCP/IP
            return "http://192.168.1.100:5000"

        case .production:
            // Production - Manajet on DigitalOcean
            return "https://pr.manajet.io"
        }
    }

    var name: String {
        switch self {
        case .development:
            return "Development"
        case .production:
            return "Production"
        }
    }

    var requiresHTTPS: Bool {
        switch self {
        case .development:
            return false
        case .production:
            return true
        }
    }
}

class Configuration {
    // MARK: - Current Environment
    // Change this line to switch environments:
    // - .development for local testing
    // - .production for DigitalOcean backend
    static let current: Environment = .production

    // MARK: - Computed Properties
    static var baseURL: String {
        return current.baseURL
    }

    static var environment: String {
        return current.name
    }

    static var isProduction: Bool {
        return current == .production
    }

    static var isDevelopment: Bool {
        return current == .development
    }

    // MARK: - Feature Flags
    // Enable/disable features per environment
    static var enableDebugLogging: Bool {
        return isDevelopment
    }

    static var showEnvironmentBadge: Bool {
        return true  // Set to false to hide environment indicator in UI
    }

    // MARK: - Network Configuration
    static var requestTimeout: TimeInterval {
        return 30.0  // seconds
    }

    static var allowsInsecureHTTP: Bool {
        return !current.requiresHTTPS
    }
}

// MARK: - Debug Helpers
extension Configuration {
    static func printConfiguration() {
        #if DEBUG
        print("""

        ╔══════════════════════════════════════╗
        ║     Manajet Configuration            ║
        ╠══════════════════════════════════════╣
        ║ Environment: \(environment.padding(toLength: 24, withPad: " ", startingAt: 0))║
        ║ Base URL: \(baseURL.padding(toLength: 27, withPad: " ", startingAt: 0))║
        ║ HTTPS Required: \(current.requiresHTTPS ? "Yes" : "No ")                    ║
        ║ Debug Logging: \(enableDebugLogging ? "Enabled " : "Disabled")              ║
        ╚══════════════════════════════════════╝

        """)
        #endif
    }
}
