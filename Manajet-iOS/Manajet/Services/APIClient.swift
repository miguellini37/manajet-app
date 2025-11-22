//
//  APIClient.swift
//  Manajet
//
//  Handles all API communication with Flask backend
//

import Foundation

class APIClient: ObservableObject {
    static let shared = APIClient()

    // MARK: - Configuration
    // Backend URL is managed in Configuration.swift
    // Change Configuration.current to switch between dev and production
    private let baseURL = Configuration.baseURL

    @Published var isAuthenticated = false
    @Published var currentUser: User?

    private var session: URLSession

    private init() {
        let config = URLSessionConfiguration.default
        config.httpCookieAcceptPolicy = .always
        config.httpShouldSetCookies = true
        config.httpCookieStorage = HTTPCookieStorage.shared
        config.timeoutIntervalForRequest = Configuration.requestTimeout
        self.session = URLSession(configuration: config)

        // Print configuration in debug mode
        Configuration.printConfiguration()
    }

    // MARK: - Authentication
    func login(username: String, password: String) async throws -> User {
        let url = URL(string: "\(baseURL)/login")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/x-www-form-urlencoded", forHTTPHeaderField: "Content-Type")

        let body = "username=\(username)&password=\(password)"
        request.httpBody = body.data(using: .utf8)

        let (data, response) = try await session.data(for: request)

        guard let httpResponse = response as? HTTPURLResponse,
              httpResponse.statusCode == 200 else {
            throw APIError.authenticationFailed
        }

        // Parse user from response or make separate API call to get user data
        // For now, we'll make a follow-up request to get current user
        return try await getCurrentUser()
    }

    func logout() async throws {
        let url = URL(string: "\(baseURL)/logout")!
        var request = URLRequest(url: url)
        request.httpMethod = "GET"

        _ = try await session.data(for: request)

        await MainActor.run {
            self.isAuthenticated = false
            self.currentUser = nil
        }
    }

    func getCurrentUser() async throws -> User {
        // This requires adding a /api/current-user endpoint to your Flask app
        let url = URL(string: "\(baseURL)/api/current-user")!
        let (data, _) = try await session.data(from: url)
        let user = try JSONDecoder().decode(User.self, from: data)

        await MainActor.run {
            self.isAuthenticated = true
            self.currentUser = user
        }

        return user
    }

    // MARK: - Flights
    func getFlights() async throws -> [Flight] {
        let url = URL(string: "\(baseURL)/api/flights")!
        let (data, _) = try await session.data(from: url)
        return try JSONDecoder().decode([Flight].self, from: data)
    }

    func scheduleFlight(
        jetId: String,
        departure: String,
        destination: String,
        departureTime: String,
        arrivalTime: String,
        passengerIds: [String],
        crewIds: [String]
    ) async throws -> String {
        let url = URL(string: "\(baseURL)/api/flights/schedule")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")

        let body: [String: Any] = [
            "jet_id": jetId,
            "departure": departure,
            "destination": destination,
            "departure_time": departureTime,
            "arrival_time": arrivalTime,
            "passenger_ids": passengerIds,
            "crew_ids": crewIds
        ]

        request.httpBody = try JSONSerialization.data(withJSONObject: body)

        let (data, response) = try await session.data(for: request)

        guard let httpResponse = response as? HTTPURLResponse,
              httpResponse.statusCode == 200 else {
            throw APIError.requestFailed
        }

        let result = try JSONDecoder().decode([String: String].self, from: data)
        guard let flightId = result["flight_id"] else {
            throw APIError.invalidResponse
        }

        return flightId
    }

    // MARK: - Approvals (Pilots)
    func getPendingApprovals() async throws -> [Flight] {
        let url = URL(string: "\(baseURL)/api/approvals/pending")!
        let (data, _) = try await session.data(from: url)
        return try JSONDecoder().decode([Flight].self, from: data)
    }

    func approveFlight(flightId: String) async throws {
        let url = URL(string: "\(baseURL)/flights/\(flightId)/approve")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"

        _ = try await session.data(for: request)
    }

    func rejectFlight(flightId: String) async throws {
        let url = URL(string: "\(baseURL)/flights/\(flightId)/reject")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"

        _ = try await session.data(for: request)
    }

    // MARK: - Jets
    func getJets() async throws -> [Jet] {
        let url = URL(string: "\(baseURL)/api/jets")!
        let (data, _) = try await session.data(from: url)
        return try JSONDecoder().decode([Jet].self, from: data)
    }

    // MARK: - Passengers
    func getPassengers() async throws -> [Passenger] {
        let url = URL(string: "\(baseURL)/api/passengers")!
        let (data, _) = try await session.data(from: url)
        return try JSONDecoder().decode([Passenger].self, from: data)
    }

    func addPassenger(
        name: String,
        passportNumber: String,
        nationality: String,
        passportExpiry: String,
        contact: String
    ) async throws -> Passenger {
        let url = URL(string: "\(baseURL)/api/passengers/add")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")

        let body: [String: String] = [
            "name": name,
            "passport_number": passportNumber,
            "nationality": nationality,
            "passport_expiry": passportExpiry,
            "contact": contact
        ]

        request.httpBody = try JSONEncoder().encode(body)

        let (data, _) = try await session.data(for: request)
        return try JSONDecoder().decode(Passenger.self, from: data)
    }

    // MARK: - Crew
    func getCrew() async throws -> [CrewMember] {
        let url = URL(string: "\(baseURL)/api/crew")!
        let (data, _) = try await session.data(from: url)
        return try JSONDecoder().decode([CrewMember].self, from: data)
    }

    // MARK: - Airports
    func searchAirports(query: String) async throws -> [Airport] {
        guard !query.isEmpty else { return [] }

        let encodedQuery = query.addingPercentEncoding(withAllowedCharacters: .urlQueryAllowed) ?? query
        let url = URL(string: "\(baseURL)/api/airports/search?q=\(encodedQuery)&limit=10")!

        let (data, _) = try await session.data(from: url)
        let response = try JSONDecoder().decode(AirportSearchResponse.self, from: data)
        return response.results
    }

    func estimateFlightDuration(departure: String, destination: String) async throws -> FlightDurationResponse {
        let url = URL(string: "\(baseURL)/api/flights/estimate-duration?departure=\(departure)&destination=\(destination)")!
        let (data, _) = try await session.data(from: url)
        return try JSONDecoder().decode(FlightDurationResponse.self, from: data)
    }

    // MARK: - Stats
    func getStats() async throws -> DashboardStats {
        let url = URL(string: "\(baseURL)/api/stats")!
        let (data, _) = try await session.data(from: url)
        return try JSONDecoder().decode(DashboardStats.self, from: data)
    }
}

// MARK: - Errors
enum APIError: LocalizedError {
    case invalidURL
    case requestFailed
    case invalidResponse
    case authenticationFailed
    case networkError(Error)

    var errorDescription: String? {
        switch self {
        case .invalidURL:
            return "Invalid URL"
        case .requestFailed:
            return "Request failed"
        case .invalidResponse:
            return "Invalid response from server"
        case .authenticationFailed:
            return "Authentication failed. Please check your credentials."
        case .networkError(let error):
            return "Network error: \(error.localizedDescription)"
        }
    }
}
