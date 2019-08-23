import Foundation

public struct GeoData {
    public let sourceName: String

    public init(sourceName: String) {
        self.sourceName = sourceName
    }
}

extension GeoData {
    public var sourceRepr: String {
        """
        GeoData(sourceName: "\(sourceName)")
        """
    }
}
