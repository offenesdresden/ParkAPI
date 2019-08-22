import Foundation

public protocol Importer {
    var name: String { get }
    var slug: String { get }

    var url: URL { get }
    var sourceURL: URL { get }
}

extension Importer {
    public var slug: String {
        return self.name.slug
    }


}

public protocol HtmlImporter: Importer { }

extension HtmlImporter {

}
