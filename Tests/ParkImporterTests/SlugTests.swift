import XCTest
@testable import ParkImporter

final class SlugTests: XCTestCase {
    func testSlug() {
        let slugs = [
            "foobar": "foobar",
            "fübar": "fuebar",
            "f ba-r": "fbar"
        ]

        for (orig, slug) in slugs {
            XCTAssertEqual(orig.slug, slug)
        }
    }

    static var allTests = [
        ("testSlug", testSlug),
    ]
}
