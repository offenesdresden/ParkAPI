import XCTest
@testable import CarPark

final class CarParkTests: XCTestCase {
    func testGetSpecificImporter() {
        let dresden = CarPark.importer(forSourceWithName: "Dresden")
        XCTAssertEqual(dresden?.url.absoluteString, "https://www.dresden.de/parken")
    }

    func testSupportedSources() {
        XCTAssertEqual(CarPark.supportedSources.count, 1)
    }

    func testDataSourceProperties() {
        for importer in CarPark.importers {
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

        for importer in CarPark.importers {
            let e = expectation(description: "Receive data for \(importer.name).")

            importer.fetch(session: .shared) { result in
                switch result {
                case .failure(let error):
                    XCTFail("Failed with error: \(error)")
                    e.fulfill()
                case .success(let dataPoint):
                    XCTAssert(!dataPoint.lots.isEmpty)
                    e.fulfill()
                }
            }

            waitForExpectations(timeout: 10)
        }
    }

    static var allTests = [
        ("testGetSpecificImporter", testGetSpecificImporter),
        ("testSupportedSources", testSupportedSources),
        ("testDataSourceProperties", testDataSourceProperties),
        ("testLiveData", testLiveData),
    ]
}
