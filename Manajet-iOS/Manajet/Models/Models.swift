//
//  Models.swift
//  Manajet
//
//  Data models matching Flask backend
//

import Foundation

// MARK: - User & Authentication
struct User: Codable, Identifiable {
    let id: String
    let username: String
    let role: UserRole
    let relatedId: String
    let email: String

    enum CodingKeys: String, CodingKey {
        case id = "user_id"
        case username
        case role
        case relatedId = "related_id"
        case email
    }
}

enum UserRole: String, Codable {
    case admin
    case customer
    case crew
    case mechanic
}

struct LoginRequest: Codable {
    let username: String
    let password: String
}

struct LoginResponse: Codable {
    let success: Bool
    let message: String?
    let user: User?
}

// MARK: - Customer
struct Customer: Codable, Identifiable {
    let id: String
    let name: String
    let company: String
    let email: String
    let phone: String
    let address: String
    let leadPilotId: String?

    enum CodingKeys: String, CodingKey {
        case id = "customer_id"
        case name, company, email, phone, address
        case leadPilotId = "lead_pilot_id"
    }
}

// MARK: - Passenger
struct Passenger: Codable, Identifiable {
    let id: String
    let name: String
    let passportNumber: String
    let nationality: String
    let passportExpiry: String
    let contact: String
    let customerId: String

    enum CodingKeys: String, CodingKey {
        case id = "passenger_id"
        case name
        case passportNumber = "passport_number"
        case nationality
        case passportExpiry = "passport_expiry"
        case contact
        case customerId = "customer_id"
    }
}

// MARK: - Crew
struct CrewMember: Codable, Identifiable {
    let id: String
    let name: String
    let crewType: String
    let passportNumber: String
    let nationality: String
    let passportExpiry: String
    let contact: String
    let licenseNumber: String?

    enum CodingKeys: String, CodingKey {
        case id = "crew_id"
        case name
        case crewType = "crew_type"
        case passportNumber = "passport_number"
        case nationality
        case passportExpiry = "passport_expiry"
        case contact
        case licenseNumber = "license_number"
    }
}

// MARK: - Jet
struct Jet: Codable, Identifiable {
    let id: String
    let model: String
    let tailNumber: String
    let capacity: Int
    let customerIds: [String]
    let status: JetStatus

    enum CodingKeys: String, CodingKey {
        case id = "jet_id"
        case model
        case tailNumber = "tail_number"
        case capacity
        case customerIds = "customer_ids"
        case status
    }
}

enum JetStatus: String, Codable {
    case available = "Available"
    case inFlight = "In Flight"
    case maintenance = "Maintenance"
}

// MARK: - Flight
struct Flight: Codable, Identifiable {
    let id: String
    let jetId: String
    let departure: String
    let destination: String
    let departureTime: String
    let arrivalTime: String
    let passengerIds: [String]
    let crewIds: [String]
    let status: FlightStatus
    let approvalStatus: ApprovalStatus
    let requestedBy: String
    let approvedBy: String?
    let approvalDate: String?

    enum CodingKeys: String, CodingKey {
        case id = "flight_id"
        case jetId = "jet_id"
        case departure, destination
        case departureTime = "departure_time"
        case arrivalTime = "arrival_time"
        case passengerIds = "passenger_ids"
        case crewIds = "crew_ids"
        case status
        case approvalStatus = "approval_status"
        case requestedBy = "requested_by"
        case approvedBy = "approved_by"
        case approvalDate = "approval_date"
    }
}

enum FlightStatus: String, Codable {
    case scheduled = "Scheduled"
    case inProgress = "In Progress"
    case completed = "Completed"
    case cancelled = "Cancelled"
}

enum ApprovalStatus: String, Codable {
    case pending = "Pending"
    case approved = "Approved"
    case rejected = "Rejected"
}

// MARK: - Airport
struct Airport: Codable, Identifiable {
    let code: String
    let name: String
    let city: String
    let state: String
    let country: String

    var id: String { code }

    var displayName: String {
        "\(code) - \(name) (\(city), \(state))"
    }
}

struct AirportSearchResponse: Codable {
    let results: [Airport]
}

struct FlightDurationResponse: Codable {
    let departure: String
    let destination: String
    let durationHours: Int
    let durationMinutes: Int
    let durationTotalMinutes: Int
    let durationText: String

    enum CodingKeys: String, CodingKey {
        case departure, destination
        case durationHours = "duration_hours"
        case durationMinutes = "duration_minutes"
        case durationTotalMinutes = "duration_total_minutes"
        case durationText = "duration_text"
    }
}

// MARK: - Dashboard Stats
struct DashboardStats: Codable {
    let totalPassengers: Int
    let totalCrew: Int
    let totalJets: Int
    let totalFlights: Int
    let activeFlights: Int
    let availableJets: Int

    enum CodingKeys: String, CodingKey {
        case totalPassengers = "total_passengers"
        case totalCrew = "total_crew"
        case totalJets = "total_jets"
        case totalFlights = "total_flights"
        case activeFlights = "active_flights"
        case availableJets = "available_jets"
    }
}
