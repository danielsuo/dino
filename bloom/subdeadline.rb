require 'rubygems'
require 'bud'

class Subdeadline
  include Bud

  state do
    table :vertex, [:vid] => [:execution]
    table :edge, [:from, :to]

    table :source, [:vid] => [:execution]
    table :sink, [:vid] => [:execution]

    table :cumulative_execution, [:vid, :value]
    table :cumulative_execution_tmp, [:vid, :value]

    table :slack, [:vid, :value]
    table :slack_tmp, [:vid, :value]
    table :remaining_slack, [:vid, :value]
    table :deadline, [:vid, :value]
  end

  bloom :init do
    source <= vertex.notin(edge, :vid => :to)
    sink <= vertex.notin(edge, :vid => :from)
  end

  bloom :forward do
    cumulative_execution_tmp <= source {|v| [v.vid, v.execution]}

    cumulative_execution_tmp <= (vertex * edge * cumulative_execution_tmp).combos(vertex.vid => edge.to, edge.from => cumulative_execution_tmp.vid) do |v, e, s|
      [v.vid, v.execution + s.value]
    end

    cumulative_execution <= cumulative_execution_tmp.argmax([:vid], :value)
  end

  bloom :backward do

    remaining_slack <= (sink * cumulative_execution).pairs(sink.vid => cumulative_execution.vid) do |v, s|
      [v.vid, @deadline]
    end

    slack_tmp <= (vertex * cumulative_execution * remaining_slack).combos(vertex.vid => remaining_slack.vid, cumulative_execution.vid => remaining_slack.vid) do |v, s, r|
      [v.vid, v.execution / s.value.to_f * (r.value - s.value)]
    end

    remaining_slack <= (slack_tmp * edge * remaining_slack * vertex).combos(slack_tmp.vid => edge.to, remaining_slack.vid => edge.to, vertex.vid => edge.to) do |l, e, r, v|
      [e.from, r.value - l.value - v.execution]
    end

    slack <= slack_tmp.argmin([:vid], :value)
    deadline <= (vertex * slack).pairs(vertex.vid => slack.vid) do |v, l|
      [v.vid, v.execution + l.value]
    end
  end

  def setDeadline(deadline)
    @deadline = deadline
  end
end

program = Subdeadline.new

# TODO: constructor throwing error; saw examples with constructor, but no dice
program.setDeadline(12)

program.vertex <+ [['a', 1],
                   ['b', 1],
                   ['c', 1],
                   ['d', 5]]

program.edge <+ [['a', 'b'],
                 ['b', 'c'],
                 ['a', 'c'],
                 ['d', 'c']]

# Add data
program.tick

def output(x, name)
  puts '%s:' % name
  x.to_a.sort.each {|t| puts t.inspect}
end

output(program.vertex, 'Vertex')
output(program.edge, 'Edge')
output(program.deadline, 'Deadline')

