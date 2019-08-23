import Foundation
import SwiftSoup

public class Dresden: HtmlImporter {
    public let name = "Dresden"
    public let url = URL(string: "https://www.dresden.de/parken")!
    public let sourceURL = URL(string: "https://apps.dresden.de/ords/f?p=1110")!

    public func parse(html: String, response: URLResponse) throws -> DataPoint {
        let doc = try SwiftSoup.parse(html)
        let dateSource = try doc.getElementById("P1_LAST_UPDATE")?.date(using: .dMy_Hms)

        var lots: [Lot] = []

        // select all tables that have a summary set, e.g. a region identifier
        for table in try doc.select("table[summary~=.+]") {
            let region = try table.attr("summary")
            if region == "Busparkplätze" { continue }

            for lotRow in try table.select("tr") {
                // Ignore section headers.
                guard try lotRow.select("th").isEmpty() else { continue }

                var lotState = Lot.State.open
                let imageDivClass = try lotRow.select("div").attr("class")
                // green, yellow and red are open
                if imageDivClass.contains("park-closed") {
                    lotState = .closed
                } else if imageDivClass.contains("blue") {
                    lotState = .noData
                }

                let lotName = try lotRow.select("td[headers=BEZEICHNUNG]").text()

                let freeStr = try lotRow.select("td[headers=FREI]").text()
                let free = Int(freeStr) ?? 0

                let totalStr = try lotRow.select("td[headers=KAPAZITAET]").text()
                let total = Int(totalStr) ?? 0 // TODO: Get fallback from geodata instead.

                let lot = Lot(name: lotName,
                              coordinates: Lot.Coordinates(latitude: 1.0, longitude: 1.0),
                              address: nil,
                              free: free,
                              state: lotState,
                              type: nil,
                              additionalInformation: nil)
                lots.append(lot)
            }
        }

        return DataPoint(dateSource: dateSource, lots: lots)
    }
}
