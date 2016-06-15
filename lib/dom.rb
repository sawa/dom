# frozen_string_literal: true

# Copyright (c) 2016 sawa

require "stringio"
require "strscan"
require "htmlentities"

class DomString < String; end

using (Module.new do
	refine String do
		AnsiColor = {
			"1" => "bold",
			"4" => "underline",
			"30" => "black",
			"31" => "red",
			"32" => "green",
			"33" => "yellow",
			"34" => "blue",
			"35" => "magenta",
			"36" => "cyan",
			"37" => "white",
			"40" => "bg-black",
			"41" => "bg-red",
			"42" => "bg-green",
			"43" => "bg-yellow",
			"44" => "bg-blue",
			"45" => "bg-magenta",
			"46" => "bg-cyan",
			"47" => "bg-white",
		}
		def dom_escape tag = nil
			case tag; when :style, :script then self else Dom::Coder.encode(self) end
		end
		def _ansi2html
			sc = StringScanner.new(self)
			io = StringIO.new
			io.print(
				if sc.scan(/\e\[0?m/o) then '</span>'
				elsif sc.scan(/\e\[0?(\d+)m/o) then '<span class="%s">' % AnsiColor[sc[1]]
				end ||
			sc.scan(/./mo)) until sc.eos?
			io.string
		end
	end

	refine DomString do
		def dom_escape tag = nil; self end
	end
end)

class File
	def self.relativize f; f.sub(%r{\A/}o, "") end
end

module Dom
	Coder = HTMLEntities.new
	Indent = "  "
	private_constant :Indent
	def self.compact; singleton_class.class_eval{alias join join_compact} end
	def self.nested; singleton_class.class_eval{alias join join_nested} end
	def self.pre; singleton_class.class_eval{alias join join_pre} end
	def self.join_compact a, tag
		a.map{|e| e.to_s.dom_escape(tag)}.join
	end
	def self.join_nested a, tag
		a.map{|e| e.to_s.dom_escape(tag).concat($/)}
		.join.gsub(/^/o, Indent)
		.prepend($/)
	end
	def self.join_pre a, tag
		a.map{|e| e.to_s.dom_escape(tag).prepend("-->").concat("<!--#$/")}
		.join.gsub(/^/o, Indent)
		.prepend("<!--#$/").concat("-->")
	end
	def self.format tag, attr
		tag = hyphenize(tag)
		[
			[
				tag,
				*attr.map do
					|k, v|
					v = case v
					when nil then next
					when false then "none"
					when true then ""
					else v
					end
					"%s=\"%s\"" % [hyphenize(k), v]
				end
			].compact.join(" "),
			tag
		]
	end
	def self.json_format tag, attr
		[
			hyphenize(tag),
			*([attr.map{|k, v| [hyphenize(k), v]}.to_h] if attr)
		]
	end
	def self.hyphenize sym; sym.to_s.tr("_", "-") end
end

module Kernel
	private def dom tag, mounted: nil, **attr
		"<%s />".%(Dom.format(tag, attr).first).dom_escaped.mounted_set(mounted)
	end
	private def jsonml tag, attr = nil
		Dom.json_format(tag, attr)
	end
end

class NilClass
	public :dom
	public :jsonml
	def mounted; nil end
end

class String
	def dom tag = nil, mounted: nil, **attr
		if tag
			"<%s>%s</%s>".%(
				Dom.format(tag, attr)
				.insert(1, (block_given? ? yield(self) : self).dom_escape(tag)._ansi2html)
			)
		else
			dom_escape
		end
		.dom_escaped.mounted_set(mounted)
	end
	def jsonml tag, attr = nil; [*Dom.json_format(tag, attr), self] end
	def mounted; nil end
	def dom_escaped; DomString.new(self) end
	def ansi2html; _ansi2html.dom_escaped end
end

class DomString < String
	def to_s; self end
	def dom_escaped; self end
	def mounted_set *mounted
		mounted.compact!
		if mounted.empty?
		elsif @mounted then @mounted.concat(mounted.join)
		else @mounted = mounted.join
		end
		self
	end
	attr_reader :mounted
end

class Array
	def dom *tags, mounted: nil, **attr
		*recurse, tag = tags
		a = self
		a = block_given? ? map(&Proc.new) : flatten if recurse.empty?
		if recurse.length <= 1
			#!index: Using `index` instead of `find` to be able to detect `nil`. 
			#   (Which turned out irrelevant.)
			if i = a.index{|e| e.kind_of?(String).! and e.kind_of?(Array).! and e.nil?.!}
				raise ArgumentError
				.new("Expecting all array elements to be a string: `#{a[i].class}:#{a[i].inspect}'")
			end
		else
			#!index:
			if i = a.index{|e| e.kind_of?(Array).!}
				raise ArgumentError
				.new("Cannot apply tag `#{recurse[-2].inspect}' to `#{a[i].class}:#{a[i].inspect}'")
			end
		end
		a = a.map{|e| e.dom(*recurse, &(Proc.new if block_given?))} unless recurse.empty?
		s = Dom.join(a, tag)
		s = "<%s>%s</%s>" % Dom.format(tag, attr).insert(1, s) unless tag.nil?
		s.dom_escaped.mounted_set(*a.map(&:mounted), mounted)
	end
	def jsonml tag, attr = nil; [*Dom.json_format(attr), *self] end
end

Dom.compact
