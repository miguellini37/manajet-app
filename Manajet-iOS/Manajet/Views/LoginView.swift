//
//  LoginView.swift
//  Manajet
//
//  Login screen with modern iOS design
//

import SwiftUI

struct LoginView: View {
    @StateObject private var viewModel = LoginViewModel()
    @State private var showingError = false

    var body: some View {
        ZStack {
            // Gradient background
            LinearGradient(
                colors: [Color(hex: "0f172a"), Color(hex: "1e293b")],
                startPoint: .topLeading,
                endPoint: .bottomTrailing
            )
            .ignoresSafeArea()

            VStack(spacing: 30) {
                Spacer()

                // Logo and title
                VStack(spacing: 16) {
                    Image(systemName: "airplane.departure")
                        .font(.system(size: 60))
                        .foregroundStyle(
                            LinearGradient(
                                colors: [.white, Color(hex: "e0e7ff")],
                                startPoint: .topLeading,
                                endPoint: .bottomTrailing
                            )
                        )

                    Text("Manajet")
                        .font(.system(size: 36, weight: .bold))
                        .foregroundStyle(
                            LinearGradient(
                                colors: [.white, Color(hex: "e0e7ff")],
                                startPoint: .leading,
                                endPoint: .trailing
                            )
                        )

                    Text("Private Jet Management")
                        .font(.subheadline)
                        .foregroundColor(.white.opacity(0.7))
                }
                .padding(.bottom, 40)

                // Login form
                VStack(spacing: 20) {
                    // Username field
                    VStack(alignment: .leading, spacing: 8) {
                        Text("Username")
                            .font(.subheadline)
                            .foregroundColor(.white.opacity(0.9))

                        TextField("", text: $viewModel.username)
                            .textFieldStyle(ModernTextFieldStyle())
                            .autocapitalization(.none)
                            .textContentType(.username)
                    }

                    // Password field
                    VStack(alignment: .leading, spacing: 8) {
                        Text("Password")
                            .font(.subheadline)
                            .foregroundColor(.white.opacity(0.9))

                        SecureField("", text: $viewModel.password)
                            .textFieldStyle(ModernTextFieldStyle())
                            .textContentType(.password)
                    }

                    // Login button
                    Button(action: {
                        Task {
                            await viewModel.login()
                            if viewModel.errorMessage != nil {
                                showingError = true
                            }
                        }
                    }) {
                        if viewModel.isLoading {
                            ProgressView()
                                .tint(.white)
                        } else {
                            Text("Sign In")
                                .font(.headline)
                                .foregroundColor(.white)
                        }
                    }
                    .frame(maxWidth: .infinity)
                    .padding()
                    .background(
                        LinearGradient(
                            colors: [Color(hex: "6366f1"), Color(hex: "8b5cf6")],
                            startPoint: .leading,
                            endPoint: .trailing
                        )
                    )
                    .cornerRadius(12)
                    .disabled(viewModel.isLoading)
                }
                .padding(.horizontal, 32)

                Spacer()
                Spacer()
            }
        }
        .alert("Login Failed", isPresented: $showingError) {
            Button("OK", role: .cancel) { }
        } message: {
            Text(viewModel.errorMessage ?? "Unknown error occurred")
        }
    }
}

// MARK: - ViewModel
@MainActor
class LoginViewModel: ObservableObject {
    @Published var username = ""
    @Published var password = ""
    @Published var isLoading = false
    @Published var errorMessage: String?

    private let apiClient = APIClient.shared

    func login() async {
        isLoading = true
        errorMessage = nil

        do {
            _ = try await apiClient.login(username: username, password: password)
        } catch {
            errorMessage = error.localizedDescription
        }

        isLoading = false
    }
}

// MARK: - Custom Text Field Style
struct ModernTextFieldStyle: TextFieldStyle {
    func _body(configuration: TextField<Self._Label>) -> some View {
        configuration
            .padding()
            .background(Color.white.opacity(0.1))
            .cornerRadius(12)
            .foregroundColor(.white)
            .overlay(
                RoundedRectangle(cornerRadius: 12)
                    .stroke(Color.white.opacity(0.2), lineWidth: 1)
            )
    }
}

// MARK: - Color Extension
extension Color {
    init(hex: String) {
        let hex = hex.trimmingCharacters(in: CharacterSet.alphanumerics.inverted)
        var int: UInt64 = 0
        Scanner(string: hex).scanHexInt64(&int)
        let a, r, g, b: UInt64
        switch hex.count {
        case 3: // RGB (12-bit)
            (a, r, g, b) = (255, (int >> 8) * 17, (int >> 4 & 0xF) * 17, (int & 0xF) * 17)
        case 6: // RGB (24-bit)
            (a, r, g, b) = (255, int >> 16, int >> 8 & 0xFF, int & 0xFF)
        case 8: // ARGB (32-bit)
            (a, r, g, b) = (int >> 24, int >> 16 & 0xFF, int >> 8 & 0xFF, int & 0xFF)
        default:
            (a, r, g, b) = (1, 1, 1, 0)
        }

        self.init(
            .sRGB,
            red: Double(r) / 255,
            green: Double(g) / 255,
            blue:  Double(b) / 255,
            opacity: Double(a) / 255
        )
    }
}

#Preview {
    LoginView()
}
