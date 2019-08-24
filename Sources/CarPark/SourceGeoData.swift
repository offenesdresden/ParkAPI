import Foundation

public struct SourceGeoData {
    public let name: String

    public init(name: String) {
        self.name = name
    }
}

extension SourceGeoData {
    public var sourceRepr: String {
        """
        SourceGeoData(name: "\(name)")
        """
    }
}
