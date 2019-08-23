import Foundation
import SwiftSoup

public class Dresden: HtmlImporter {
    public let name = "Dresden"
    public let url = URL(string: "https://www.dresden.de/parken")!
    public let sourceURL = URL(string: "https://apps.dresden.de/ords/f?p=1110")!

    public func parse(html: String, response: URLResponse) throws -> DataPoint {
        let doc: Document = try SwiftSoup.parse(html)
        let dateSourceString = try doc.getElementById("P1_LAST_UPDATE")?.text() ?? ""
        let dateSource = DateFormatter.dMy_Hms.date(from: dateSourceString)

        return DataPoint(dateSource: dateSource, lots: [])
    }
}
