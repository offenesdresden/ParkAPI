import Foundation

extension String {
    public var slug: String {
        let replacements = [
            "ä": "ae",
            "ö": "oe",
            "ü": "ue",
            "ß": "ss",
            "-": "",
            " ": "",
            ".": "",
            ",": "",
            "'": "",
            "\"": "",
            "/": "",
            "\\": "",
            "\n": "",
            "\t": ""
        ]

        var copy = self
        for (char, repl) in replacements {
            copy = copy.replacingOccurrences(of: char, with: repl)
        }
        return copy
    }
}
