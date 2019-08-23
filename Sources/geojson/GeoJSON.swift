import Foundation

struct GeoJson: Decodable {
    let type: String
    let features: [Feature]

    struct Feature: Decodable {
        let type: String
        let geometry: Geometry
        let properties: Properties

        struct Geometry: Decodable {
            let type: String
            let coordinates: [Double]
        }

        struct Properties: Decodable {
            let name: String
            let type: String
            let url: URL?
            let source: URL?
            let activeSupport: Bool?
            let address: String?
            let total: Int?
        }
    }
}
