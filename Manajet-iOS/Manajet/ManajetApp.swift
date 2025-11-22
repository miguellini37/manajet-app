//
//  ManajetApp.swift
//  Manajet
//
//  App entry point
//

import SwiftUI

@main
struct ManajetApp: App {
    @StateObject private var apiClient = APIClient.shared

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(apiClient)
        }
    }
}

struct ContentView: View {
    @EnvironmentObject var apiClient: APIClient

    var body: some View {
        if apiClient.isAuthenticated {
            DashboardView()
        } else {
            LoginView()
        }
    }
}
