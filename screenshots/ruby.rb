module A
    def self.included(base)
        p base
    end

    def stuff(a, b)
        a * b
    end
end

class B
    attr_accessor :e
    include A

    def new
        @e = 5
    end
end

c = B.new
name = "b"
p "Hello world, #{name}"
p c.stuff(1, 2)