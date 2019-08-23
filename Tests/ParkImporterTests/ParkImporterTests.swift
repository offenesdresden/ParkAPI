import XCTest
@testable import ParkImporter

final class ParkImporterTests: XCTestCase {
    func testStaticData() {
        for importer in ParkImporter.importers {
            XCTAssert(!importer.name.isEmpty)
            XCTAssert(!importer.slug.isEmpty)
            XCTAssert(!importer.url.absoluteString.isEmpty)
            XCTAssert(!importer.sourceURL.absoluteString.isEmpty)
        }
    }

    func testLiveData() {
        for importer in ParkImporter.importers {
            let e = expectation(description: "Receive data")

            importer.fetch(session: .shared) { result in
                switch result {
                case .failure(let error):
                    XCTFail("Failed with error: \(error)")
                    e.fulfill()
                case .success(let dataPoint):
                    e.fulfill()
                }
            }

            waitForExpectations(timeout: 10)
        }
    }

    static var allTests = [
        ("testStaticData", testStaticData),
        ("testLiveData", testLiveData),
    ]
}
