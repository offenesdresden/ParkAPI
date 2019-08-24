import Foundation
import Files
import CarPark

func readGeoData() throws -> [GeoJson] {
    let geojsonFiles = try Folder(path: "Sources/CarPark/DataSources").files
        .filter { $0.name.contains("geojson") }
    let decoder = JSONDecoder()
    decoder.keyDecodingStrategy = .convertFromSnakeCase
    return try geojsonFiles.map { try decoder.decode(GeoJson.self, from: $0.read()) }
}

func write(geoData: [GeoJson]) throws {
    let geoData = [SourceGeoData(name: "Dresden")]
    let fileContent = """
    // This file is auto-generated, do not edit.
    // Run `swift run geojson` instead.

    let geoData = [
        \(geoData.map { $0.sourceRepr }.joined(separator: ",\n"))
    ]

    """
    try File(path: "Sources/CarPark/Geo.swift").write(string: fileContent)
}

let geoData = try readGeoData()
try write(geoData: geoData)
