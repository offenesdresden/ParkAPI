import XCTest
@testable import ParkImporter

final class ParkImporterTests: XCTestCase {
    func testGetSpecificImporter() {
        let dresden = ParkImporter.importer(forSourceWithName: "Dresden")
        XCTAssertEqual(dresden?.url.absoluteString, "https://www.dresden.de/parken")
    }

    func testSupportedSources() {
        XCTAssertEqual(ParkImporter.supportedSources.count, 1)
    }

    func testStaticData() {
        for importer in ParkImporter.importers {
            XCTAssert(!importer.name.isEmpty)
            XCTAssert(!importer.slug.isEmpty)
            XCTAssert(!importer.url.absoluteString.isEmpty)
            XCTAssert(!importer.sourceURL.absoluteString.isEmpty)
        }
    }

    func testLiveData() {
        guard !(ProcessInfo.processInfo.environment["TEST_LIVE"]?.isEmpty ?? true) else {
            print("Skipping live tests, set TEST_LIVE environment variable to enable.")
            return
        }

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
        ("testGetSpecificImporter", testGetSpecificImporter),
        ("testStaticData", testStaticData),
        ("testLiveData", testLiveData),
    ]
}
