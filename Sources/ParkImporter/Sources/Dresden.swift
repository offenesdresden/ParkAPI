import Foundation
import SwiftSoup

public class Dresden: HtmlImporter {
    public let name = "Dresden"
    public let url = URL(string: "https://www.dresden.de/parken")!
    public let sourceURL = URL(string: "https://apps.dresden.de/ords/f?p=1110")!

    public func parse(html: String, response: URLResponse) throws -> DataPoint {
        let doc = try SwiftSoup.parse(html)
        let dateSource = try doc.getElementById("P1_LAST_UPDATE")?.date(using: .dMy_Hms)

        for table in try doc.select("table.uReportAlternative") {
            print(try table.attr("summary"))
        }

        return DataPoint(dateSource: dateSource, lots: [])
    }
}
