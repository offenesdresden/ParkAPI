public struct Lot {
    public let name: String
    public let coordinates: Coordinates
    public let address: String?
    public let free: Int
    public let total: Int? // TODO: Possibly rename to capacity?
    public let state: State
    public let type: Type?
    public let additionalInformation: [String: Any]?

    public init(name: String,
                coordinates: Coordinates,
                address: String?,
                free: Int,
                total: Int?,
                state: Lot.State,
                type: Lot.`Type`?,
                additionalInformation: [String : Any]? = nil) {
        self.name = name
        self.coordinates = coordinates
        self.address = address
        self.free = free
        self.total = total
        self.state = state
        self.type = type
        self.additionalInformation = additionalInformation
    }
}

extension Lot {
    public struct Coordinates {
        public let latitude: Double
        public let longitude: Double
    }

    public enum State {
        case open, closed, noData
    }

    public enum `Type` {
        case lot, structure, underground
    }
}
