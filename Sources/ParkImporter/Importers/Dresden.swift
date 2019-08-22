import Foundation
import SwiftSoup

public class Dresden: HtmlImporter {
    public let name = "Dresden"
    public let url = URL(string: "https://www.dresden.de/parken")!
    public let sourceURL = URL(string: "https://apps.dresden.de/ords/f?p=1110")!

    internal init() {}

    public func parse(html: String, response: URLResponse) throws -> LotInformation {
        let doc: Document = try SwiftSoup.parse(html)
        print(try doc.text())

        return LotInformation(dateSource: Date(), lots: [])
    }
}
