//
//  DashboardView.swift
//  Manajet
//
//  Main dashboard with stats and navigation
//

import SwiftUI

struct DashboardView: View {
    @StateObject private var viewModel = DashboardViewModel()
    @EnvironmentObject var apiClient: APIClient

    var body: some View {
        NavigationView {
            ScrollView {
                VStack(spacing: 24) {
                    // Welcome header
                    VStack(alignment: .leading, spacing: 8) {
                        Text("Welcome back,")
                            .font(.title3)
                            .foregroundColor(.secondary)

                        if let user = apiClient.currentUser {
                            Text(user.username)
                                .font(.system(size: 32, weight: .bold))
                        }
                    }
                    .frame(maxWidth: .infinity, alignment: .leading)
                    .padding()

                    // Stats grid
                    if let stats = viewModel.stats {
                        LazyVGrid(columns: [
                            GridItem(.flexible()),
                            GridItem(.flexible())
                        ], spacing: 16) {
                            StatCard(
                                title: "Active Flights",
                                value: "\(stats.activeFlights)",
                                icon: "airplane",
                                color: .blue
                            )

                            StatCard(
                                title: "Available Jets",
                                value: "\(stats.availableJets)",
                                icon: "airplane.departure",
                                color: .green
                            )

                            StatCard(
                                title: "Total Passengers",
                                value: "\(stats.totalPassengers)",
                                icon: "person.2",
                                color: .purple
                            )

                            StatCard(
                                title: "Crew Members",
                                value: "\(stats.totalCrew)",
                                icon: "person.3",
                                color: .orange
                            )
                        }
                        .padding(.horizontal)
                    }

                    // Quick actions
                    VStack(alignment: .leading, spacing: 16) {
                        Text("Quick Actions")
                            .font(.headline)
                            .padding(.horizontal)

                        VStack(spacing: 12) {
                            NavigationLink(destination: FlightScheduleView()) {
                                QuickActionRow(
                                    icon: "plus.circle.fill",
                                    title: "Schedule New Flight",
                                    subtitle: "Book a new flight",
                                    color: .blue
                                )
                            }

                            NavigationLink(destination: FlightsListView()) {
                                QuickActionRow(
                                    icon: "list.bullet",
                                    title: "View All Flights",
                                    subtitle: "See your flight schedule",
                                    color: .purple
                                )
                            }

                            if apiClient.currentUser?.role == .crew {
                                NavigationLink(destination: ApprovalsView()) {
                                    QuickActionRow(
                                        icon: "checkmark.circle.fill",
                                        title: "Pending Approvals",
                                        subtitle: "Review flight requests",
                                        color: .orange,
                                        badge: viewModel.pendingApprovalsCount
                                    )
                                }
                            }

                            NavigationLink(destination: PassengersListView()) {
                                QuickActionRow(
                                    icon: "person.2.fill",
                                    title: "Manage Passengers",
                                    subtitle: "View and add passengers",
                                    color: .green
                                )
                            }
                        }
                        .padding(.horizontal)
                    }
                }
                .padding(.vertical)
            }
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button(action: {
                        Task {
                            try? await apiClient.logout()
                        }
                    }) {
                        Image(systemName: "rectangle.portrait.and.arrow.right")
                    }
                }
            }
            .task {
                await viewModel.loadData()
            }
            .refreshable {
                await viewModel.loadData()
            }
        }
    }
}

// MARK: - Stat Card
struct StatCard: View {
    let title: String
    let value: String
    let icon: String
    let color: Color

    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            HStack {
                Image(systemName: icon)
                    .font(.title2)
                    .foregroundColor(color)
                Spacer()
            }

            Text(value)
                .font(.system(size: 28, weight: .bold))

            Text(title)
                .font(.subheadline)
                .foregroundColor(.secondary)
        }
        .padding()
        .frame(maxWidth: .infinity, alignment: .leading)
        .background(Color(.systemBackground))
        .cornerRadius(16)
        .shadow(color: .black.opacity(0.05), radius: 10, x: 0, y: 4)
    }
}

// MARK: - Quick Action Row
struct QuickActionRow: View {
    let icon: String
    let title: String
    let subtitle: String
    let color: Color
    var badge: Int? = nil

    var body: some View {
        HStack(spacing: 16) {
            ZStack(alignment: .topTrailing) {
                Image(systemName: icon)
                    .font(.title2)
                    .foregroundColor(color)
                    .frame(width: 50, height: 50)
                    .background(color.opacity(0.1))
                    .cornerRadius(12)

                if let badge = badge, badge > 0 {
                    Text("\(badge)")
                        .font(.caption2.bold())
                        .foregroundColor(.white)
                        .padding(.horizontal, 6)
                        .padding(.vertical, 2)
                        .background(Color.red)
                        .cornerRadius(10)
                        .offset(x: 8, y: -8)
                }
            }

            VStack(alignment: .leading, spacing: 4) {
                Text(title)
                    .font(.headline)
                    .foregroundColor(.primary)

                Text(subtitle)
                    .font(.subheadline)
                    .foregroundColor(.secondary)
            }

            Spacer()

            Image(systemName: "chevron.right")
                .foregroundColor(.secondary)
        }
        .padding()
        .background(Color(.systemBackground))
        .cornerRadius(12)
        .shadow(color: .black.opacity(0.05), radius: 8, x: 0, y: 2)
    }
}

// MARK: - ViewModel
@MainActor
class DashboardViewModel: ObservableObject {
    @Published var stats: DashboardStats?
    @Published var pendingApprovalsCount: Int = 0
    @Published var isLoading = false

    private let apiClient = APIClient.shared

    func loadData() async {
        isLoading = true

        async let statsTask = try? apiClient.getStats()
        async let approvalsTask = apiClient.currentUser?.role == .crew
            ? (try? apiClient.getPendingApprovals())
            : nil

        stats = await statsTask
        if let approvals = await approvalsTask {
            pendingApprovalsCount = approvals.count
        }

        isLoading = false
    }
}

// Placeholder views - will be created next
struct FlightsListView: View {
    var body: some View {
        Text("Flights List")
            .navigationTitle("Flights")
    }
}

struct PassengersListView: View {
    var body: some View {
        Text("Passengers List")
            .navigationTitle("Passengers")
    }
}

#Preview {
    DashboardView()
        .environmentObject(APIClient.shared)
}
