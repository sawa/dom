Gem::Specification.new do
	|s|
	s.name = "dom"
	s.version = "1.0.1"
	s.date = "2016-04-04"
	s.authors = ["sawa"]
	s.email = []
	s.license = "MIT"
	s.summary = "A library to generate HTML/XML code from Ruby commands. It replaces conventional approcaches using template engines, or certain kind of libraries with a similar purpose."
	s.description = "You can describe HTML/XML structures in Ruby language seamlessly with other parts of Ruby code. Node embedding is described as method chaining, which avoids unnecessary nesting, and confirms to the Rubyistic coding style."
	s.homepage = "http://www.rubymanager.com/rubydom/"
	s.metadata = {
		"issue_tracker" => "https://github.com/sawa/dom"
	}
	s.files = Dir["*.html"] + ["license", "spec", "lib/dom.rb"]
	s.add_runtime_dependency "htmlentities", ">= 0"
	s.add_development_dependency "manager", ">= 0"
end
