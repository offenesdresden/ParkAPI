import Foundation
import SwiftSoup

public class Dresden: HtmlImporter {
    public let name = "Dresden"
    public let url = URL(string: "https://www.dresden.de/parken")!
    public let sourceURL = URL(string: "https://apps.dresden.de/ords/f?p=1110")!

    public func parse(html: String, response: URLResponse) throws -> DataPoint {
        let doc = try SwiftSoup.parse(html)
        let dateSource = try doc.getElementById("P1_LAST_UPDATE")?.date(using: .dMy_Hms)

        // Select all tables that have a summary field set (a region identifier).
        let lots = try doc.select("table[summary~=.+]")
            .filter { try $0.attr("summary") != "Busparkplätze" }
            .map { try $0.select("tr").compactMap(extract(lotFrom:)) }
            .flatMap { $0 }

        return DataPoint(dateSource: dateSource, lots: lots)
    }

    private func extract(lotFrom row: Element) throws -> Lot? {
        // Ignore section headers.
        guard try row.select("th").isEmpty() else { return nil }

        var lotState = Lot.State.open
        let imageDivClass = try row.select("div").attr("class")
        // green, yellow and red are open, blue is no data, park-closed is... closed
        if imageDivClass.contains("park-closed") {
            lotState = .closed
        } else if imageDivClass.contains("blue") {
            lotState = .noData
        }

        let lotName = try row.select("td[headers=BEZEICHNUNG]").text()
        let free = try row.select("td[headers=FREI]").int(else: 0)
        // TODO: Get fallback from geodata instead.
        // Or maybe put that and coordinate lookup into Lot initializer when params are nil?
        let total = try row.select("td[headers=KAPAZITAET]").int()

        return Lot(name: lotName,
                   coordinates: Lot.Coordinates(latitude: 1.0, longitude: 1.0),
                   address: nil,
                   free: free,
                   total: total,
                   state: lotState,
                   type: nil)
    }
}
