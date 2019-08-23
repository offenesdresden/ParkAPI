import Foundation

public struct DataPoint {
    public let dateDownloaded: Date
    public let dateSource: Date?
    public let lots: [Lot]

    public init(dateDownloaded: Date = Date(), dateSource: Date?, lots: [Lot]) {
        self.dateDownloaded = dateDownloaded
        self.dateSource = dateSource
        self.lots = lots
    }
}

public struct Lot {
    public let name: String
    public let coordinates: Coordinates
    public let address: String?
    public let free: Int
    public let state: State
    public let additionalInformation: [String: Any]?

    public init(name: String,
                coordinates: Coordinates,
                address: String?,
                free: Int,
                state: Lot.State,
                additionalInformation: [String : Any]? = nil) {
        self.name = name
        self.coordinates = coordinates
        self.address = address
        self.free = free
        self.state = state
        self.additionalInformation = additionalInformation
    }
}

extension Lot {
    public enum State {
        case open
        case closed
        case noData
    }

    public struct Coordinates {
        public let latitude: Double
        public let longitude: Double
    }
}
