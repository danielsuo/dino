require 'rubygems'
require 'bud'

class Subdeadline
  include Bud

  state do
    # Table of all vertices with their execution times
    table :vertex, [:vid] => [:execution]

    # Table of all edges between vertices
    table :edge, [:from, :to]

    # Table of source nodes
    table :source, [:vid] => [:execution]

    # Table of sink nodes
    table :sink, [:vid] => [:execution]

    # TODO: Data normalized here since tables above shouldn't really be
    # modified that often, but in general, should we be normalizing data and having
    # so many tables?
    # TODO: is it better to use a temporary table rather than delete/insert/wait a tick?
    
    # Forward pass tables
    scratch :cumulative_execution, [:vid, :value]
    scratch :cumulative_execution_tmp, [:vid, :value]

    # Backward pass tables
    scratch :slack, [:vid, :value]
    scratch :slack_tmp, [:vid, :value]
    scratch :remaining, [:vid, :value]
    scratch :deadline, [:vid, :value]
  end

  # Collect source and sink vertexs
  bloom :init do
    source <= vertex.notin(edge, :vid => :to)
    sink <= vertex.notin(edge, :vid => :from)
  end

  # Forward pass of Algorithm 1. This is essentially a longest path
  # algorithm, but the cost is on the vertexs instead on the edges. Conceptually
  # similar (except the extra vertex at the end), but a little less nice than
  # if cost were on the edges.
  bloom :forward do

    # Initialize with source vertices
    cumulative_execution_tmp <= source {|v| [v.vid, v.execution]}

    # Recursively build paths from sources to sinks
    cumulative_execution_tmp <= (vertex * edge * cumulative_execution_tmp).combos(vertex.vid => edge.to, edge.from => cumulative_execution_tmp.vid) do |v, e, s|
      [v.vid, v.execution + s.value]
    end

    # Extract max path for each vertex
    cumulative_execution <= cumulative_execution_tmp.argmax([:vid], :value)
  end

  # Backward pass of Algorithm 1. Divide up slack time among all nodes along
  # each path.
  bloom :backward do

    # Initialize with sink vertices
    remaining <= sink {|v| [v.vid, @deadline]}

    # Compute amount of slack to allocate a vertex
    slack_tmp <= (vertex * cumulative_execution * remaining).combos(vertex.vid => remaining.vid, cumulative_execution.vid => remaining.vid) do |v, s, r|
      [v.vid, v.execution / s.value.to_f * (r.value - s.value)]
    end

    # Compute amount of time remaining for the beginning of a path
    remaining <= (slack_tmp * edge * remaining * vertex).combos(slack_tmp.vid => edge.to, remaining.vid => edge.to, vertex.vid => edge.to) do |l, e, r, v|
      [e.from, r.value - l.value - v.execution]
    end

    # Extract min slack for each vertex
    slack <= slack_tmp.argmin([:vid], :value)

    # The deadline is just slack plus execution time
    deadline <= (vertex * slack).pairs(vertex.vid => slack.vid) do |v, l|
      [v.vid, v.execution + l.value]
    end
  end

  # TODO: constructor throwing error; saw examples with constructor, but no dice
  def setDeadline(deadline)
    @deadline = deadline
  end
end

# Creating our program
program = Subdeadline.new
program.setDeadline(12)

# Initializing vertices and edges
program.vertex <+ [['a', 1],
                   ['b', 1],
                   ['c', 1],
                   ['d', 5]]

program.edge <+ [['a', 'b'],
                 ['b', 'c'],
                 ['a', 'c'],
                 ['d', 'c']]

# Add data and compute
program.tick

def output(x, name)
  puts '%s:' % name
  x.to_a.sort.each {|t| puts t.inspect}
end

output(program.vertex, 'Vertex')
output(program.edge, 'Edge')
output(program.deadline, 'Deadline')

