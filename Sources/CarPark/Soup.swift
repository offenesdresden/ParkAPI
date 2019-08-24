import Foundation
import SwiftSoup

extension Element {
    func date(using formatter: DateFormatter) -> Date? {
        let text = (try? self.text()) ?? ""
        return formatter.date(from: text)
    }
}

extension Elements {
    func int() throws -> Int? {
        let text = (try? self.text()) ?? ""
        return Int(text)
    }

    func int(else: Int) throws -> Int {
        let text = (try? self.text()) ?? ""
        return Int(text) ?? `else`
    }
}
