import Foundation

extension DateFormatter {
    static var dMy_Hms: DateFormatter {
        let df = DateFormatter()
        df.dateFormat = "dd.MM.yyyy HH:mm:ss"
        return df
    }
}
