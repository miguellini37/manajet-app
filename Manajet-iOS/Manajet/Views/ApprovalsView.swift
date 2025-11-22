//
//  ApprovalsView.swift
//  Manajet
//
//  Flight approval workflow for pilots
//

import SwiftUI

struct ApprovalsView: View {
    @StateObject private var viewModel = ApprovalsViewModel()

    var body: some View {
        Group {
            if viewModel.isLoading {
                ProgressView()
            } else if viewModel.pendingFlights.isEmpty {
                // Empty state
                VStack(spacing: 20) {
                    Image(systemName: "checkmark.circle.fill")
                        .font(.system(size: 60))
                        .foregroundColor(.green)

                    Text("All Caught Up!")
                        .font(.title.bold())

                    Text("No pending flight approvals at this time.")
                        .foregroundColor(.secondary)
                        .multilineTextAlignment(.center)
                }
                .padding()
            } else {
                // List of pending approvals
                List {
                    ForEach(viewModel.pendingFlights) { flight in
                        FlightApprovalCard(flight: flight) {
                            viewModel.selectedFlight = flight
                        }
                    }
                }
                .listStyle(.plain)
            }
        }
        .navigationTitle("Pending Approvals")
        .navigationBarTitleDisplayMode(.inline)
        .task {
            await viewModel.loadPendingFlights()
        }
        .refreshable {
            await viewModel.loadPendingFlights()
        }
        .sheet(item: $viewModel.selectedFlight) { flight in
            FlightApprovalDetailView(flight: flight) {
                await viewModel.loadPendingFlights()
            }
        }
        .alert("Error", isPresented: $viewModel.showingError) {
            Button("OK", role: .cancel) { }
        } message: {
            Text(viewModel.errorMessage ?? "Unknown error")
        }
    }
}

// MARK: - Flight Approval Card
struct FlightApprovalCard: View {
    let flight: Flight
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            VStack(alignment: .leading, spacing: 12) {
                // Header
                HStack {
                    VStack(alignment: .leading, spacing: 4) {
                        Text("Flight \(flight.id)")
                            .font(.headline)

                        Text("\(flight.departure) → \(flight.destination)")
                            .font(.title3.bold())
                            .foregroundColor(.primary)
                    }

                    Spacer()

                    Badge(text: "PENDING", color: .orange)
                }

                Divider()

                // Flight details
                VStack(spacing: 8) {
                    InfoRow(icon: "calendar", label: "Departure", value: formatDateTime(flight.departureTime))
                    InfoRow(icon: "clock", label: "Arrival", value: formatDateTime(flight.arrivalTime))
                    InfoRow(icon: "person.2", label: "Passengers", value: "\(flight.passengerIds.count)")
                    InfoRow(icon: "person.3", label: "Crew", value: "\(flight.crewIds.count)")
                }

                // Action hint
                HStack {
                    Spacer()
                    Label("Tap to review", systemImage: "arrow.right.circle.fill")
                        .font(.subheadline)
                        .foregroundColor(.blue)
                }
            }
            .padding()
            .background(Color(.systemBackground))
            .cornerRadius(12)
            .shadow(color: .black.opacity(0.05), radius: 8, x: 0, y: 2)
        }
        .buttonStyle(.plain)
        .listRowSeparator(.hidden)
        .listRowBackground(Color.clear)
    }

    func formatDateTime(_ dateString: String) -> String {
        // Simple formatter - you might want to enhance this
        dateString.replacingOccurrences(of: "T", with: " ")
    }
}

// MARK: - Flight Approval Detail View
struct FlightApprovalDetailView: View {
    let flight: Flight
    let onAction: () async -> Void

    @Environment(\.dismiss) var dismiss
    @State private var isLoading = false
    @State private var showingApproveConfirm = false
    @State private var showingRejectConfirm = false

    var body: some View {
        NavigationView {
            ScrollView {
                VStack(spacing: 24) {
                    // Route header
                    VStack(spacing: 8) {
                        Text("\(flight.departure) → \(flight.destination)")
                            .font(.system(size: 28, weight: .bold))

                        Badge(text: "PENDING APPROVAL", color: .orange)
                    }
                    .padding()

                    // Flight details card
                    VStack(alignment: .leading, spacing: 16) {
                        SectionHeader(title: "Flight Details")

                        DetailRow(label: "Flight ID", value: flight.id)
                        DetailRow(label: "Departure", value: flight.departureTime)
                        DetailRow(label: "Arrival", value: flight.arrivalTime)
                        DetailRow(label: "Aircraft", value: flight.jetId)
                        DetailRow(label: "Status", value: flight.status.rawValue)
                    }
                    .padding()
                    .background(Color(.systemBackground))
                    .cornerRadius(12)
                    .shadow(color: .black.opacity(0.05), radius: 8, x: 0, y: 2)

                    // Passengers card
                    VStack(alignment: .leading, spacing: 16) {
                        SectionHeader(title: "Passengers (\(flight.passengerIds.count))")

                        if flight.passengerIds.isEmpty {
                            Text("No passengers")
                                .foregroundColor(.secondary)
                        } else {
                            ForEach(flight.passengerIds, id: \.self) { passengerId in
                                HStack {
                                    Image(systemName: "person.circle.fill")
                                        .foregroundColor(.blue)
                                    Text("Passenger ID: \(passengerId)")
                                    Spacer()
                                }
                            }
                        }
                    }
                    .padding()
                    .background(Color(.systemBackground))
                    .cornerRadius(12)
                    .shadow(color: .black.opacity(0.05), radius: 8, x: 0, y: 2)

                    // Crew card
                    VStack(alignment: .leading, spacing: 16) {
                        SectionHeader(title: "Crew (\(flight.crewIds.count))")

                        ForEach(flight.crewIds, id: \.self) { crewId in
                            HStack {
                                Image(systemName: "person.fill.checkmark")
                                    .foregroundColor(.green)
                                Text("Crew ID: \(crewId)")
                                Spacer()
                            }
                        }
                    }
                    .padding()
                    .background(Color(.systemBackground))
                    .cornerRadius(12)
                    .shadow(color: .black.opacity(0.05), radius: 8, x: 0, y: 2)

                    // Action buttons
                    VStack(spacing: 12) {
                        Button(action: { showingApproveConfirm = true }) {
                            Label("Approve Flight", systemImage: "checkmark.circle.fill")
                                .font(.headline)
                                .foregroundColor(.white)
                                .frame(maxWidth: .infinity)
                                .padding()
                                .background(Color.green)
                                .cornerRadius(12)
                        }
                        .disabled(isLoading)

                        Button(action: { showingRejectConfirm = true }) {
                            Label("Reject Flight", systemImage: "xmark.circle.fill")
                                .font(.headline)
                                .foregroundColor(.white)
                                .frame(maxWidth: .infinity)
                                .padding()
                                .background(Color.red)
                                .cornerRadius(12)
                        }
                        .disabled(isLoading)
                    }
                    .padding(.horizontal)
                }
                .padding()
            }
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("Close") { dismiss() }
                }
            }
        }
        .confirmationDialog("Approve Flight?", isPresented: $showingApproveConfirm) {
            Button("Approve", role: .destructive) {
                Task {
                    await approveFlight()
                }
            }
        } message: {
            Text("Are you sure you want to approve this flight?")
        }
        .confirmationDialog("Reject Flight?", isPresented: $showingRejectConfirm) {
            Button("Reject", role: .destructive) {
                Task {
                    await rejectFlight()
                }
            }
        } message: {
            Text("Are you sure you want to reject this flight request?")
        }
    }

    func approveFlight() async {
        isLoading = true
        defer { isLoading = false }

        do {
            try await APIClient.shared.approveFlight(flightId: flight.id)
            await onAction()
            dismiss()
        } catch {
            print("Error approving flight: \(error)")
        }
    }

    func rejectFlight() async {
        isLoading = true
        defer { isLoading = false }

        do {
            try await APIClient.shared.rejectFlight(flightId: flight.id)
            await onAction()
            dismiss()
        } catch {
            print("Error rejecting flight: \(error)")
        }
    }
}

// MARK: - Supporting Views
struct SectionHeader: View {
    let title: String

    var body: some View {
        Text(title)
            .font(.headline)
            .foregroundColor(.secondary)
            .textCase(.uppercase)
    }
}

struct DetailRow: View {
    let label: String
    let value: String

    var body: some View {
        HStack {
            Text(label)
                .foregroundColor(.secondary)
            Spacer()
            Text(value)
                .fontWeight(.medium)
        }
    }
}

struct InfoRow: View {
    let icon: String
    let label: String
    let value: String

    var body: some View {
        HStack(spacing: 12) {
            Image(systemName: icon)
                .foregroundColor(.blue)
                .frame(width: 20)

            Text(label)
                .foregroundColor(.secondary)
                .frame(width: 80, alignment: .leading)

            Text(value)
                .fontWeight(.medium)

            Spacer()
        }
    }
}

struct Badge: View {
    let text: String
    let color: Color

    var body: some View {
        Text(text)
            .font(.caption.bold())
            .foregroundColor(.white)
            .padding(.horizontal, 12)
            .padding(.vertical, 6)
            .background(color)
            .cornerRadius(8)
    }
}

// MARK: - ViewModel
@MainActor
class ApprovalsViewModel: ObservableObject {
    @Published var pendingFlights: [Flight] = []
    @Published var selectedFlight: Flight?
    @Published var isLoading = false
    @Published var showingError = false
    @Published var errorMessage: String?

    private let apiClient = APIClient.shared

    func loadPendingFlights() async {
        isLoading = true
        defer { isLoading = false }

        do {
            pendingFlights = try await apiClient.getPendingApprovals()
        } catch {
            errorMessage = error.localizedDescription
            showingError = true
        }
    }
}

#Preview {
    NavigationView {
        ApprovalsView()
    }
}
