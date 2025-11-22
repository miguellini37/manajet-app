//
//  FlightScheduleView.swift
//  Manajet
//
//  Schedule new flight with location search and flexible time selection
//

import SwiftUI

struct FlightScheduleView: View {
    @StateObject private var viewModel = FlightScheduleViewModel()
    @Environment(\.dismiss) var dismiss

    var body: some View {
        Form {
            // Aircraft selection
            Section("Aircraft") {
                Picker("Select Aircraft", selection: $viewModel.selectedJetId) {
                    Text("Select aircraft...").tag(nil as String?)
                    ForEach(viewModel.jets) { jet in
                        Text("\(jet.model) (\(jet.tailNumber))").tag(jet.id as String?)
                    }
                }
            }

            // Location search
            Section("Route") {
                // Departure
                VStack(alignment: .leading, spacing: 8) {
                    Text("Departure Location")
                        .font(.subheadline)
                        .foregroundColor(.secondary)

                    AirportSearchField(
                        query: $viewModel.departureQuery,
                        selectedAirport: $viewModel.selectedDeparture,
                        airports: viewModel.departureResults
                    )

                    if let airport = viewModel.selectedDeparture {
                        Text(airport.displayName)
                            .font(.caption)
                            .foregroundColor(.secondary)
                    }
                }

                // Destination
                VStack(alignment: .leading, spacing: 8) {
                    Text("Destination Location")
                        .font(.subheadline)
                        .foregroundColor(.secondary)

                    AirportSearchField(
                        query: $viewModel.destinationQuery,
                        selectedAirport: $viewModel.selectedDestination,
                        airports: viewModel.destinationResults
                    )

                    if let airport = viewModel.selectedDestination {
                        Text(airport.displayName)
                            .font(.caption)
                            .foregroundColor(.secondary)
                    }
                }

                // Flight duration info
                if let duration = viewModel.flightDuration {
                    HStack {
                        Image(systemName: "clock.fill")
                            .foregroundColor(.blue)
                        Text("Estimated flight time: \(duration.durationText)")
                            .font(.subheadline)
                        Spacer()
                    }
                    .padding(.vertical, 8)
                    .padding(.horizontal, 12)
                    .background(Color.blue.opacity(0.1))
                    .cornerRadius(8)
                }
            }

            // Time selection method
            Section("Timing") {
                Picker("Time Method", selection: $viewModel.timeMethod) {
                    Text("I know when I want to depart").tag(TimeMethod.departAt)
                    Text("I know when I need to arrive").tag(TimeMethod.arriveBy)
                }
                .pickerStyle(.segmented)

                if viewModel.timeMethod == .departAt {
                    DatePicker(
                        "Departure Time",
                        selection: $viewModel.departureTime,
                        displayedComponents: [.date, .hourAndMinute]
                    )

                    if viewModel.arrivalTime != nil {
                        HStack {
                            Text("Arrival Time")
                            Spacer()
                            Text(viewModel.arrivalTime!.formatted(date: .abbreviated, time: .shortened))
                                .foregroundColor(.secondary)
                        }
                    }
                } else {
                    DatePicker(
                        "Arrival Time",
                        selection: $viewModel.arrivalTime ?? Date(),
                        displayedComponents: [.date, .hourAndMinute]
                    )
                    .onChange(of: viewModel.arrivalTime) { _, _ in
                        viewModel.calculateDepartureTime()
                    }

                    if let departureTime = viewModel.departureTime {
                        HStack {
                            Text("Departure Time")
                            Spacer()
                            Text(departureTime.formatted(date: .abbreviated, time: .shortened))
                                .foregroundColor(.secondary)
                        }
                    }
                }
            }

            // Passengers
            Section("Passengers") {
                ForEach(viewModel.passengers) { passenger in
                    MultipleSelectionRow(
                        title: passenger.name,
                        subtitle: passenger.passportNumber,
                        isSelected: viewModel.selectedPassengerIds.contains(passenger.id)
                    ) {
                        if viewModel.selectedPassengerIds.contains(passenger.id) {
                            viewModel.selectedPassengerIds.removeAll { $0 == passenger.id }
                        } else {
                            viewModel.selectedPassengerIds.append(passenger.id)
                        }
                    }
                }

                Button(action: { viewModel.showingAddPassenger = true }) {
                    Label("Add New Passenger", systemImage: "plus.circle.fill")
                }
            }

            // Crew
            Section("Crew (Pilot Required)") {
                ForEach(viewModel.crew) { crewMember in
                    MultipleSelectionRow(
                        title: crewMember.name,
                        subtitle: crewMember.crewType,
                        isSelected: viewModel.selectedCrewIds.contains(crewMember.id),
                        badge: crewMember.crewType == "Pilot" ? "PILOT" : nil
                    ) {
                        if viewModel.selectedCrewIds.contains(crewMember.id) {
                            viewModel.selectedCrewIds.removeAll { $0 == crewMember.id }
                        } else {
                            viewModel.selectedCrewIds.append(crewMember.id)
                        }
                    }
                }

                if !viewModel.hasPilotSelected {
                    Label("At least one pilot must be selected", systemImage: "exclamationmark.triangle.fill")
                        .foregroundColor(.orange)
                        .font(.caption)
                }
            }
        }
        .navigationTitle("Schedule Flight")
        .navigationBarTitleDisplayMode(.inline)
        .toolbar {
            ToolbarItem(placement: .navigationBarTrailing) {
                Button("Schedule") {
                    Task {
                        let success = await viewModel.scheduleFlight()
                        if success {
                            dismiss()
                        }
                    }
                }
                .disabled(!viewModel.canSchedule || viewModel.isLoading)
            }
        }
        .task {
            await viewModel.loadData()
        }
        .alert("Error", isPresented: $viewModel.showingError) {
            Button("OK", role: .cancel) { }
        } message: {
            Text(viewModel.errorMessage ?? "Unknown error")
        }
        .sheet(isPresented: $viewModel.showingAddPassenger) {
            AddPassengerView(onAdd: { passenger in
                viewModel.passengers.append(passenger)
                viewModel.selectedPassengerIds.append(passenger.id)
            })
        }
    }
}

// MARK: - Airport Search Field
struct AirportSearchField: View {
    @Binding var query: String
    @Binding var selectedAirport: Airport?
    let airports: [Airport]

    @State private var showingResults = false

    var body: some View {
        VStack(alignment: .leading, spacing: 0) {
            TextField("Type city name or airport code", text: $query)
                .textFieldStyle(.roundedBorder)
                .onChange(of: query) { _, _ in
                    showingResults = !query.isEmpty && selectedAirport == nil
                }

            if showingResults && !airports.isEmpty {
                VStack(alignment: .leading, spacing: 0) {
                    ForEach(airports) { airport in
                        Button(action: {
                            selectedAirport = airport
                            query = airport.code
                            showingResults = false
                        }) {
                            VStack(alignment: .leading, spacing: 4) {
                                Text(airport.code)
                                    .font(.headline)
                                Text("\(airport.name) (\(airport.city), \(airport.state))")
                                    .font(.caption)
                                    .foregroundColor(.secondary)
                            }
                            .padding(.vertical, 8)
                            .padding(.horizontal, 12)
                            .frame(maxWidth: .infinity, alignment: .leading)
                        }
                        .buttonStyle(.plain)

                        if airport.id != airports.last?.id {
                            Divider()
                        }
                    }
                }
                .background(Color(.systemBackground))
                .cornerRadius(8)
                .shadow(radius: 4)
            }
        }
    }
}

// MARK: - Multiple Selection Row
struct MultipleSelectionRow: View {
    let title: String
    let subtitle: String
    let isSelected: Bool
    var badge: String? = nil
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            HStack {
                VStack(alignment: .leading, spacing: 4) {
                    HStack {
                        Text(title)
                            .foregroundColor(.primary)
                        if let badge = badge {
                            Text(badge)
                                .font(.caption2.bold())
                                .padding(.horizontal, 6)
                                .padding(.vertical, 2)
                                .background(Color.blue)
                                .foregroundColor(.white)
                                .cornerRadius(4)
                        }
                    }
                    Text(subtitle)
                        .font(.caption)
                        .foregroundColor(.secondary)
                }

                Spacer()

                if isSelected {
                    Image(systemName: "checkmark.circle.fill")
                        .foregroundColor(.blue)
                } else {
                    Image(systemName: "circle")
                        .foregroundColor(.gray)
                }
            }
        }
    }
}

// MARK: - Time Method
enum TimeMethod {
    case departAt
    case arriveBy
}

// MARK: - ViewModel
@MainActor
class FlightScheduleViewModel: ObservableObject {
    @Published var jets: [Jet] = []
    @Published var passengers: [Passenger] = []
    @Published var crew: [CrewMember] = []

    @Published var selectedJetId: String?
    @Published var departureQuery = ""
    @Published var destinationQuery = ""
    @Published var selectedDeparture: Airport?
    @Published var selectedDestination: Airport?
    @Published var departureResults: [Airport] = []
    @Published var destinationResults: [Airport] = []
    @Published var flightDuration: FlightDurationResponse?

    @Published var timeMethod: TimeMethod = .departAt
    @Published var departureTime = Date()
    @Published var arrivalTime: Date?

    @Published var selectedPassengerIds: [String] = []
    @Published var selectedCrewIds: [String] = []

    @Published var isLoading = false
    @Published var showingError = false
    @Published var errorMessage: String?
    @Published var showingAddPassenger = false

    private let apiClient = APIClient.shared
    private var searchTask: Task<Void, Never>?

    var hasPilotSelected: Bool {
        selectedCrewIds.contains { id in
            crew.first(where: { $0.id == id })?.crewType == "Pilot"
        }
    }

    var canSchedule: Bool {
        selectedJetId != nil &&
        selectedDeparture != nil &&
        selectedDestination != nil &&
        !selectedCrewIds.isEmpty &&
        hasPilotSelected
    }

    init() {
        setupSearchObservers()
    }

    func setupSearchObservers() {
        // Debounce search queries
        Task { @MainActor in
            for await query in $departureQuery.values.debounce(for: .milliseconds(300)) {
                await searchDepartureAirports(query: query)
            }
        }

        Task { @MainActor in
            for await query in $destinationQuery.values.debounce(for: .milliseconds(300)) {
                await searchDestinationAirports(query: query)
            }
        }
    }

    func loadData() async {
        do {
            async let jetsTask = apiClient.getJets()
            async let passengersTask = apiClient.getPassengers()
            async let crewTask = apiClient.getCrew()

            jets = try await jetsTask.filter { $0.status == .available }
            passengers = try await passengersTask
            crew = try await crewTask
        } catch {
            errorMessage = error.localizedDescription
            showingError = true
        }
    }

    func searchDepartureAirports(query: String) async {
        guard !query.isEmpty else {
            departureResults = []
            return
        }

        do {
            departureResults = try await apiClient.searchAirports(query: query)
        } catch {
            print("Search error: \(error)")
        }
    }

    func searchDestinationAirports(query: String) async {
        guard !query.isEmpty else {
            destinationResults = []
            return
        }

        do {
            destinationResults = try await apiClient.searchAirports(query: query)

            // Auto-calculate flight duration when both selected
            if let dep = selectedDeparture, let dest = selectedDestination {
                try await calculateFlightDuration(from: dep.code, to: dest.code)
            }
        } catch {
            print("Search error: \(error)")
        }
    }

    func calculateFlightDuration(from departure: String, to destination: String) async throws {
        flightDuration = try await apiClient.estimateFlightDuration(
            departure: departure,
            destination: destination
        )

        // Auto-calculate arrival/departure time based on method
        if timeMethod == .departAt {
            calculateArrivalTime()
        } else {
            calculateDepartureTime()
        }
    }

    func calculateArrivalTime() {
        guard let duration = flightDuration else { return }
        arrivalTime = departureTime.addingTimeInterval(TimeInterval(duration.durationTotalMinutes * 60))
    }

    func calculateDepartureTime() {
        guard let duration = flightDuration, let arrival = arrivalTime else { return }
        departureTime = arrival.addingTimeInterval(-TimeInterval(duration.durationTotalMinutes * 60))
    }

    func scheduleFlight() async -> Bool {
        guard canSchedule else { return false }

        isLoading = true
        defer { isLoading = false }

        do {
            let dateFormatter = DateFormatter()
            dateFormatter.dateFormat = "yyyy-MM-dd HH:mm"

            let finalArrivalTime = arrivalTime ?? departureTime.addingTimeInterval(3600)

            _ = try await apiClient.scheduleFlight(
                jetId: selectedJetId!,
                departure: selectedDeparture!.code,
                destination: selectedDestination!.code,
                departureTime: dateFormatter.string(from: departureTime),
                arrivalTime: dateFormatter.string(from: finalArrivalTime),
                passengerIds: selectedPassengerIds,
                crewIds: selectedCrewIds
            )

            return true
        } catch {
            errorMessage = error.localizedDescription
            showingError = true
            return false
        }
    }
}

// MARK: - Add Passenger View
struct AddPassengerView: View {
    @Environment(\.dismiss) var dismiss
    let onAdd: (Passenger) -> Void

    @State private var name = ""
    @State private var passportNumber = ""
    @State private var nationality = ""
    @State private var passportExpiry = Date()
    @State private var contact = ""
    @State private var isLoading = false
    @State private var errorMessage: String?

    var body: some View {
        NavigationView {
            Form {
                TextField("Full Name", text: $name)
                TextField("Passport Number", text: $passportNumber)
                TextField("Nationality", text: $nationality)
                DatePicker("Passport Expiry", selection: $passportExpiry, displayedComponents: .date)
                TextField("Contact (Email or Phone)", text: $contact)
            }
            .navigationTitle("Add Passenger")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("Cancel") { dismiss() }
                }
                ToolbarItem(placement: .confirmationAction) {
                    Button("Add") {
                        Task {
                            await addPassenger()
                        }
                    }
                    .disabled(isLoading || name.isEmpty || passportNumber.isEmpty)
                }
            }
        }
    }

    func addPassenger() async {
        isLoading = true
        defer { isLoading = false }

        do {
            let dateFormatter = DateFormatter()
            dateFormatter.dateFormat = "yyyy-MM-dd"

            let passenger = try await APIClient.shared.addPassenger(
                name: name,
                passportNumber: passportNumber,
                nationality: nationality,
                passportExpiry: dateFormatter.string(from: passportExpiry),
                contact: contact
            )

            onAdd(passenger)
            dismiss()
        } catch {
            errorMessage = error.localizedDescription
        }
    }
}

// MARK: - Publisher Extension for Debounce
extension Published.Publisher {
    var values: AsyncStream<Value> {
        AsyncStream { continuation in
            let cancellable = sink { value in
                continuation.yield(value)
            }
            continuation.onTermination = { _ in
                cancellable.cancel()
            }
        }
    }
}

extension AsyncSequence {
    func debounce<C: Clock>(for duration: C.Instant.Duration, clock: C = ContinuousClock()) -> AsyncStream<Element> {
        AsyncStream { continuation in
            let task = Task {
                var lastValue: Element?
                var lastTime = clock.now

                for await value in self {
                    lastValue = value
                    lastTime = clock.now

                    try? await clock.sleep(for: duration)

                    if clock.now >= lastTime + duration {
                        if let value = lastValue {
                            continuation.yield(value)
                            lastValue = nil
                        }
                    }
                }

                continuation.finish()
            }

            continuation.onTermination = { _ in
                task.cancel()
            }
        }
    }
}

#Preview {
    NavigationView {
        FlightScheduleView()
    }
}
