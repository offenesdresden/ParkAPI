import SwiftSoup

extension Element {
    func date(using formatter: DateFormatter) -> Date? {
        let text = (try? self.text()) ?? ""
        return formatter.date(from: text)
    }
}
