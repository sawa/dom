# frozen_string_literal: false
#!ruby

Manager.config(spell_check: "en")

Manager.config(case_insensitive: %w[
dom
json
jsonml
merchantability
noninfringement
rubyistic
sawa
sublicense
])

gemspec "dom.gemspec"
manage "lib/dom.rb"

spec "=License",
	"The MIT License (MIT)",
	"Copyright (c) 2013-2016 sawa",
	"Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the \"Software\"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:",
	"The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.",
	"THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.",
coda

spec "=Overview",
	"Dom gem is a library to generate HTML or XML code from Ruby commands. It replaces the conventional approach that uses template engines and conventional Ruby libraries used for generating HTML or XML strings.",
	"Here are some problems with the conventional tools:",
	"1. With template engines, you need to write the HTML or XML code in a language different from the language used for the program (Ruby), and you need to write it either in a file distinct from the Ruby program, or as a here document in the Ruby program.",
	"2. Some conventional Ruby libraries use commands that are named after the type of the DOM node. Notations with such libraries may look like:",
	<<~'RUBY'.code,
		h1{"Hello World!"} # => "<h1>Hello World!</h1>"
		div{"Hello World!"} # => "<div>Hello World!</div>"
	RUBY
	"This approach is not flexible; for every type of node, the corresponding command needs to be defined in advance in the library to be usable. A user would not be able to use an original node type that is not predefined in the library.",
	"3. Some conventional Ruby libraries accept the content of a node as a block. Nested nodes would then require nested blocks:",
	<<~'RUBY'.code,
		div{p{span{"Hello World!"}}}
		# => "<div><p><span>Hello World!</span></p></div>"
	RUBY
	"As the structure becomes complicated, it becomes more difficult to keep track of paring between the opening and the closing of the blocks.",
	"Dom gem solves these problems that the conventional tools have. In particular,",
	"1. With Dom gem, you can describe HTML and XML structures in Ruby language seamlessly with other parts of Ruby code.",
	"2. Dom gem uses a fixed method name `dom`, which takes a symbol argument that represents the node type. The equivalent of the first sample above in dom would be:",
	<<~'RUBY'.code,
		"Hello World!".dom(:h1) # => "<h1>Hello World!</h1>"
		"Hello World!".dom(:div) # => "<div>Hello World!</div>"
	RUBY
	"3. In dom, the content of a node is the receiver of the method `dom`. Node embedding is described as method chaining. This avoids unnecessary nesting, and confirms to the Rubyistic coding style. The equivalent of the second sample above in dom would be:",
	<<~'RUBY'.code,
		"Hello World!".dom(:span).dom(:p).dom(:div)
		# => "<div><p><span>Hello World!</span></p></div>"
	RUBY
coda

spec "=Usage",
	"Require dom:",
	<<~'RUBY'.code,
		require "dom"
	RUBY
	"To surround a string with a tag, use the `dom` method. Pass the tag name as a symbol, with an optional hash, whose keys are symbols, and values that are either `nil`, `true`, `false`, or other kinds of objects that have the `to_s` methods implemented.",
		<<~'RUBY'.code,
			"foo".dom(:span, class: "bar")
			# => "<span class=\"bar\">foo</span>"

			"foo".dom(:span, data_1: nil, data_2: 3)
			# => "<span data-2=\"3\">foo</span>"
		RUBY
		"The `dom` method can be chained to generate nested structures.",
		<<~'RUBY'.code,
			"Hello World!".dom(:span).dom(:p).dom(:div)
			# => "<div><p><span>Hello World!</span></p></div>"
		RUBY
		"When `dom` applies to an array, its elements are joined.",
		<<~'RUBY'.code,
				["foo", "bar"].dom(:div, class: "bar")
				# => "<div class=\"bar\">foobar</div>"
		RUBY
		"When multiple tags are passed to a single `dom` method call, the tags are distributed and are percolated into the nested arrays.",
		<<~'RUBY'.code,
			[["foo1", "foo2"], ["bar1", "bar2"]].dom(:td, :tr, :table)
			# => "<table><tr><td>foo1</td><td>foo2</td></tr><tr><td>bar1</td><td>bar2</td></tr></table>"
		RUBY
coda

spec "=Contribution",
	"To access to the source code or to contribute, please access {https://github.com/sawa/dom}.",
	"The developer information of Dom gem is available at {http://www.rubymanager.com/rubydom/CHART.html}.",
coda

module Dom
	hide spec "::Coder",
	coda

	hide spec "::Indent",
		"! Indentation internally used in `join` when the mode is `nested` or `pre`.",
		UT =~ /\s+/,
	coda

	spec ".compact",
		{"()" => value(nil)},
		"Sets the output to compact mode. This is usually the best for production use. It is compressed, and is not convenient for human reading. This is the default mode.",
		UT.succeed?,
		"Dom.compact".setup,
		<<~'RUBY'.code,
			Dom.compact
			[["foo1", "foo2"], ["bar1", "bar2"]].dom(:td, :tr)
			# => "<tr><td>foo1foo2</td><td>bar1bar2</td></tr>"
		RUBY
	coda

	spec ".nested",
		{"()" => value(nil)},
		"Sets the output to nested mode. This is usually the best for development use. It may not be optimized for production use.",
		UT.succeed?,
		"Dom.compact".setup,
		<<~'RUBY'.code,
			Dom.nested
			[["foo1", "foo2"], ["bar1", "bar2"]].dom(:td, :tr)
			# => "<tr>\n  <td>\n    foo1\n    foo2\n  </td>\n  <td>\n    bar1\n    bar2\n  </td>\n</tr>"
	RUBY
	coda

		hide spec ".pre",
		"! Inserts HTML's comment expressions. This is for special usage. Normally, you will not need to to set to this mode.",
		UT.succeed?,
		"Dom.compact".setup,
		<<~'RUBY'.code!,
			Dom.pre
			[["foo1", "foo2"], ["bar1", "bar2"]].dom(:td, :tr)
			# => "<tr><!--\n  --><td><!--\n    -->foo1<!--\n    -->foo2<!--\n  --></td><!--\n  --><td><!--\n    -->bar1<!--\n    -->bar2<!--\n  --></td><!--\n--></tr>"
		RUBY
	coda

	hide spec ".join_compact",
		"! Internally used `join` method for `compact` mode.",
	coda

	hide spec ".join_nested",
		"! Internally used `join` method for `nested` mode.",
	coda

	hide spec ".join_pre",
		"! Internally used `join` method for `pre` mode.",
	coda

	hide spec ".format",
		"! Converts a hash into an HTML attribute. An attribute `:foo` with value `true` and `false` will be converted to the string `foo=\"\"` and `foo=\"none\"`, respectively. Key-value pairs with the value `nil` will be excluded from the output. Other values will be applied `to_s`. The pairs will be joined by a space, and the whole string will be prefixed by a space.",
		UT(:script, foo: "abcabc") == ["script foo=\"abcabc\"", "script"],
		UT(:div, foo: nil) == ["div", "div"],
		UT(:div, foo: false) == ["div foo=\"none\"", "div"],
		UT(:script, foo: true) == ["script foo=\"\"", "script"],
		UT(:div, foo: 3) == ["div foo=\"3\"", "div"],
		UT(:div, foo1: "abcabc", foo2: nil, foo3: false, foo4: true, foo5: 3) ==
		["div foo1=\"abcabc\" foo3=\"none\" foo4=\"\" foo5=\"3\"", "div"],
	coda

	hide spec ".json_format",
		"! Creates an array to be used in JSON.",
		UT(:div, style: "foo") == ["div", {"style" => "foo"}],
	coda

	hide spec ".hyphenize",
		"!Converts underscore into hyphen. Used in `json_format`.",
		UT("FooBar_Baz-Foo") == "FooBar-Baz-Foo",
	coda

	hide spec ".join",
		"! Joins strings in an array. Depending on the mode, either aliased to `join_compact`, `join_nested`, or `join_pre`.",
	coda
end

class String
	spec "#dom",
		{"(tag, mounted: nil, **attr)" => DomString},
		"When `dom` is called on a string, it will create a tag that includes the string as the content.",
		<<~'RUBY'.code,
			"foo".dom(:span, class: "bar")
			# => "<span class=\"bar\">foo</span>"
		RUBY
		"foo".UT(:span, class: "bar") == "<span class=\"bar\">foo</span>",
		"Attributes should be passed as a hash. A key `:foo` with value `true` or `false` will be converted to the string `foo=\"\"` or `foo=\"none\"`, respectively. Key-value pairs with the value `nil` will be excluded from the output. For other values, `to_s` will be applied.",
		<<~'RUBY'.code,
			"foo".dom(:span, data_1: nil, data_2: 3)
			# => "<span data-2=\"3\">foo</span>"
		RUBY
		"foo".UT(:span, data_1: nil, data_2: 3) == "<span data-2=\"3\">foo</span>",
		"HTML escaping will be automatically applied unless the `tag` is `:script` or `:style`:",
		<<~'RUBY'.code,
			"<".dom(:span)
			# => "<span>&lt;</span>"

			"if(3 < 5){alert('foo')};".dom(:script)
			# => "<script>if(3 < 5){alert('foo')};</script>"
		RUBY
	coda

	hide spec "#mounted",
		"! Gets the state of inner elements, namely whether they are mounted once. For `String`, this is `nil`.",
		"fresh string".UT.nil?,
	coda

#	hide spec "#dom_escape",
#		"<".UT == "&lt;",
#		"&".UT == "&amp;",
#	coda

	spec "#dom_escaped",
		{"()" => DomString},
		"Marks `self` so that it will not be further HTML escaped. Internally, it is converted to an instance of `DomString` class, which is never further escaped.",
	"When a string is already HTML escaped but has not been done so  via the `dom` method, further applying `dom` to that string without applying `dom_escaped` will incorrectly doubly apply HTML escaping:",
		<<~'RUBY'.code,
			"3 &lt; 5".dom(:span)
			# => "<span>3 &amp;lt; 5</span>"

			["foo".dom(:span, class: "bold"), "bar".dom(:span, class: "bold")].join(", ").dom(:span)
			# => "<span>&lt;span class=&quot;bold&quot;&gt;foo&lt;/span&gt;, &lt;span class=&quot;bold&quot;&gt;bar&lt;/span&gt;</span>"
		RUBY
		"To get the correct results, `dom_escaped` must be applied before `dom`:",
		<<~'RUBY'.code,
			"3 &lt; 5".dom_escaped.dom(:span)
			# => "<span>3 &lt; 5</span>"

			["foo".dom(:span, class: "bold"), "bar".dom(:span, class: "bold")].join(", ").dom_escaped.dom(:span)
			# => "<span><span class=\"bold\">foo</span>, <span class=\"bold\">bar</span></span>"
		RUBY
		" 3 &lt; 5".UT.dom(:span) == " 3 &lt; 5".dom_escaped.dom(:span),
		["a".dom(:span, class: "bold"), "b"].join.UT.dom == "<span class=\"bold\">a</span>b",
		"When the string is created by `dom` method, such consideration is unnecessary (although it will not harm if `dom_escaped` is redundantly applied).",
		<<~'RUBY'.code,
			["a".dom(:span, class: "bold"), "b"].dom.dom
			# => "<span class=\"bold\">a</span>b"
		RUBY
		" 3 &lt; 5".UT.dom(:span) == " 3 &lt; 5".dom_escaped.dom(:span),
		["a".dom(:span, class: "bold"), "b"].join.UT.dom == "<span class=\"bold\">a</span>b",
		"foo".UT.instance_of?(DomString),
		"a = \"foo\"".setup,
		expr("a").UT == expr("a"),
		expr("a").UT === expr("a"),
		expr("a").UT.eql?(expr("a")),
	coda

	hide spec "#jsonml",
	coda

	hide spec "::AnsiColor",
	coda

	hide spec "#ansi2html",
		"! Internally called by `ansi2html`.",
	coda
end

hide spec "::DomString",
coda

class DomString
	hide spec "#to_s",
		"! A `DomString` instance behaves like a `String` except that dom escape does not modify it. This class is to mark that the instance has already gone under dom escaping so that further application of dom escaping does not have effect. It makes dom escaping idempotent.",
		expr("DomString.new").UT.instance_of?(DomString),
		"a = DomString.new(\"foo\")".setup,
		expr("a").UT == expr("a"),
		expr("a").UT === expr("a"),
		expr("a").UT.eql?(expr("a")),
	coda

#	hide spec "#dom_escape",
#	coda

	spec "#dom",
		"foo".dom_escaped.UT(:span, class: "bar") == "<span class=\"bar\">foo</span>",
	coda

	spec "#dom_escaped",
		expr("DomString.new(\"foo\")").UT.instance_of?(DomString),
	coda

	hide spec "#mounted",
		"! Gets the mounted state of `self`. This is a flag indicating whether the string-like object has once been mounted in the web browser.",
	coda

	hide spec "#mounted_set",
		"! Sets the state of inner elements, namely whether they are mounted once.",
	coda
end

module Kernel
	spec "#dom",
		{"(tag, mounted: nil, **attr)" => DomString},
		"When `dom` is used without an explicit receiver, it will create a self-closing tag.",
		<<~'RUBY'.code,
			dom(:img, source: "/tmp/foo.png")
			# => "<img source=\"/tmp/foo.png\" />"
		RUBY
		"In the following example, `Kernel#dom` is called at the embedded level. See `Array#dom`.",
		<<~'RUBY'.code,
			Array.new(3).dom(:col, :colgroup)
			# => "<colgroup><col /><col /><col /></colgroup>"
		RUBY
		TOPLEVEL_BINDING.receiver.UT(:img, source: "/tmp/foo.png") == "<img source=\"/tmp/foo.png\" />",
		nil.UT(:foo) == "<foo />",
	coda

	hide spec "#jsonml",
		"! Generates a jsonml string.",
	coda
end

hide spec "::NilClass",
coda

class NilClass
	hide spec "#mounted",
		"! Gets the state of inner elements, namely whether they are mounted once. For `NilClass`, this is `nil`.",
		nil.UT.nil?,
	coda
end

class Array
	spec "#dom",
		{"(tag, mounted: nil, **attr)" => DomString},
		"Concatenates the elements and puts them inside the tag.",
		<<~'RUBY'.code,
				["foo", "bar"].dom(:div, class: "bar")
				# => "<div class=\"bar\">foobar</div>"
		RUBY
		["foo", "bar"].UT(:div, class: "bar")  == "<div class=\"bar\">foobar</div>",
		{"()" => DomString},
		"When no argument is given or an explicit `nil` is given, it joins its elements.",
		<<~'RUBY'.code,
			["foo", "bar"].dom
			# => "foobar",

			["foo", "bar"].dom(nil)
			# => "foobar",
		RUBY
		["foo", "bar"].UT == "foobar",
		RETURN.is_a?(DomString),
		["foo", "bar"].UT(nil) == "foobar",
		RETURN.is_a?(DomString),
		{"(*tags, mounted: nil, **attr)" => DomString},
		"When more than one tag is provided, it applies `dom` to each of its elements with the tags  passed except for the last tag (with no other parameters). The last tag and the other parameters are used to apply `dom` to the result.",
		<<~'RUBY'.code,
			[["foo1", "foo2"], ["bar1", "bar2"]].dom(:td, :tr, :table)
			# => "<table><tr><td>foo1</td><td>foo2</td></tr><tr><td>bar1</td><td>bar2</td></tr></table>"

			Array.new(3).dom(:col, :colgroup)
			# => "<colgroup><col /><col /><col /></colgroup>"

			[[["a", "b"], "c"], "d"].dom(:bar, :foo)
			# => "<foo><bar>abc</bar><bar>d</bar></foo>"
	RUBY
		[["foo1", "foo2"], ["bar1", "bar2"]].UT(:td, :tr, :table) ==
			"<table><tr><td>foo1</td><td>foo2</td></tr><tr><td>bar1</td><td>bar2</td></tr></table>",
		RETURN.is_a?(DomString),
		expr("Array.new(3)").UT(:col, :colgroup) == "<colgroup><col /><col /><col /></colgroup>",
#		note "flatten", "This is necessary so that `mounted` can be applied to all its elements, which is only defined for `String` and `DomString`."
		[[["a", "b"], "c"], "d"].UT(:bar, :foo) == "<foo><bar>abc</bar><bar>d</bar></foo>",
	"The array must be at least as deep as the number of tags, and the elements at that level must all be strings or arrays.",
	<<~'RUBY'.code,
			["x"].dom(:a, :b, :c, :d)
			# => ArgumentError

			[["a", 1], ["b", "c"]].dom(:td, :tr)
			# => ArgumentError
	RUBY
		["x"].UT(:a, :b, :c, :d).raise?(ArgumentError, message: /Cannot apply tag/),
		[["a", 1], ["b", "c"]].UT(:td, :tr).raise?(ArgumentError),
	"Passing `nil` as the last argument:",
		<<~'RUBY'.code,
			[["foo1", "foo2"], ["bar1", "bar2"]].dom(:td, :tr, nil)
			# => "<tr><td>foo1</td><td>foo2</td></tr><tr><td>bar1</td><td>bar2</td></tr>"

			[["a", "b"], ["c", "d"]].dom(:div, nil, nil)
			# => "<div>a</div><div>b</div><div>c</div><div>d</div>"

			[["a", "b"], ["c", "d"]].dom(:div, nil)
			# => "<div>ab</div><div>cd</div>"
		RUBY
		[["foo1", "foo2"], ["bar1", "bar2"]].UT(:td, :tr, nil) ==
		"<tr><td>foo1</td><td>foo2</td></tr><tr><td>bar1</td><td>bar2</td></tr>",
		RETURN.is_a?(DomString),
		[["a", "b"], ["c", "d"]].UT(:div, nil, nil) == "<div>a</div><div>b</div><div>c</div><div>d</div>",
		[["a", "b"], ["c", "d"]].UT(:div, nil) == "<div>ab</div><div>cd</div>",
		"Cf.",
		<<~'RUBY'.code,
			[["a", "b"], ["c", "d"]].dom(nil, :div)
			# => "<div>abcd</div>"
		RUBY
		[["a", "b"], ["c", "d"]].UT(nil, :div) == "<div>abcd</div>",
		{"(*tags, mounted: nil, **attr, &pr)" => DomString},
		"When a block is passed, the block is applied to the array at the depth depending on the class of the receiver that corresponds to the inner most tag.",
		"When the receiver that corresponds to the innermost tag is a string, the block is applied to it.",
		<<~'RUBY'.code,
			[["a", "b"], ["c", "d"]].dom(:td, :tr, :tbody){|e| e * 2} 
			# => "<tbody><tr><td>aa</td><td>bb</td></tr><tr><td>cc</td><td>dd</td></tr></tbody>"
		RUBY
		[["a", "b"], ["c", "d"]].UT(:td, :tr, :tbody){|e| e * 2} == "<tbody><tr><td>aa</td><td>bb</td></tr><tr><td>cc</td><td>dd</td></tr></tbody>",
		"When the receiver that corresponds to the innermost tag is an array, the block is applied to each of its elements.",
		<<~'RUBY'.code,
			["a", "b"].dom(:foo){|e| e * 2}
			# => "<foo>aabb</foo>"

			[["a", "b"], ["c", "d"]].dom(:bar, :foo){|e| e * 2}
			# => "<foo><bar>aabb</bar><bar>ccdd</bar></foo>"
		RUBY
		["foo", "bar"].UT(:div, class: "bar") == "<div class=\"bar\">foobar</div>",
		RETURN.is_a?(DomString),
		["a", "b"].UT(:foo){|e| e * 2} == "<foo>aabb</foo>",
		[["a", "b"], ["c", "d"]].UT(:bar, :foo){|e| e * 2} == "<foo><bar>aabb</bar><bar>ccdd</bar></foo>",
	coda

	hide spec "#jsonml",
	coda
end

class File
	spec ".relativize",
		{"(string)" => String},
		"Removes the initial slash if an absolute path is given. If a relative path is given, it has no effect.",
		<<~'RUBY'.code,
			File.relativize("/foo/bar/baz")
			# => "foo/bar/baz"

			File.relativize("foo/bar/baz")
			# => "foo/bar/baz"

			dom(:img, src: File.relativize("/foo/resource/picture.png"))
			# => "<img src=\"foo/resource/picture.png\" />"
		RUBY
		UT("/foo/bar/baz") == "foo/bar/baz",
		UT("foo/bar/baz") == "foo/bar/baz",
	coda
end
