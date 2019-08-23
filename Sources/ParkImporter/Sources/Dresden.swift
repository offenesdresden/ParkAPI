import Foundation
import SwiftSoup

public class Dresden: HtmlImporter {
    public let name = "Dresden"
    public let url = URL(string: "https://www.dresden.de/parken")!
    public let sourceURL = URL(string: "https://apps.dresden.de/ords/f?p=1110")!

    public func parse(html: String, response: URLResponse) throws -> DataPoint {
        let doc = try SwiftSoup.parse(html)
        let dateSource = try doc.getElementById("P1_LAST_UPDATE")?.date(using: .dMy_Hms)

        // select all tables that have a summary set, e.g. a region identifier
        for table in try doc.select("table[summary~=.+]") {
            let region = try table.attr("summary")
            if region == "Busparkplätze" { continue }

            print("== \(region)")
            for lotRow in try table.select("tr") {
                print(try lotRow.text())
            }
            print()
        }

        return DataPoint(dateSource: dateSource, lots: [])
    }
}
