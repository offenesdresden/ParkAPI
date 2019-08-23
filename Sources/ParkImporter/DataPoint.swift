import Foundation

public struct DataPoint {
    public let dateDownloaded: Date
    public let dateSource: Date?
    public let lots: [Lot]

    public init(dateDownloaded: Date = Date(), dateSource: Date?, lots: [Lot]) {
        self.dateDownloaded = dateDownloaded
        self.dateSource = dateSource
        self.lots = lots
    }
}
