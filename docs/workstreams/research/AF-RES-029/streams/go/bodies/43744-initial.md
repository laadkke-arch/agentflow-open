I propose extending the [Go benchmark format](https://go.googlesource.com/proposal/+/master/design/14313-benchmark-format.md) with a way to specify properties of units. Especially now that the `testing` package supports reporting custom metrics, it would be useful for tools that process benchmark results to understand basic properties of custom units in benchmark results. For example, there are two unit properties I would like for `benchstat`: 1. whether higher or lower values are better, and 2. whether measurements come from some underlying distribution (e.g., performance measurements) or are exact (e.g., file sizes).

I don't have strong opinions about the syntax. I would like the syntax for this to make sense both in the benchmark format itself, and on the command line of tools. To have something concrete, I propose the following for the benchmark format
<pre>
Unit <i>unit</i> <i>key</i>=<i>value</i> <i>key</i>=<i>value</i> ...
</pre>
and the following for command-line flags
<pre>
-unit "<i>unit</i> <i>key</i>=<i>value</i> <i>key</i>=<i>value</i> ..."
</pre>

Starting the line with `Unit` parallels how benchmark result lines start with `Benchmark`. Using `key=value` parallels both flag syntax and benchmark name configuration. An obvious alternate would be `key:value`, but this seems too similar without being the same as file-level benchmark configuration, which requires whitespace after the colon (it's unfortunate that benchmark name configuration uses `=` instead of `:`). Another option is `-key=value` to exactly parallel flag syntax, but that gets awkward when nested on the command line and raises the question of whether we also support `-key value`.

I propose it is an error to specify conflicting properties about a unit.

I also propose that a unit property applies to all following benchmark results, and that it is unspecified whether it applies to earlier benchmark results. The tools I have built that would benefit from unit properties aggregate all results before presenting them, so unit properties naturally apply to all results. But I don't want to force purely streaming tools to read all results before emitting anything just in case there's a later unit property line. Alternatively, we could say it's an error if a property is supplied for any unit that's already been seen, but this seems overly restrictive for aggregating tools.

For specific properties, I propose

1. `{higher,lower}={better,worse}` for indicating direction. Graphs and tables are often labeled "higher is better" or "lower is better", and this is meant to parallel that. I propose supporting all four combinations so people don't have to remember which works.

2. `assume={nothing,exact}` for specifying statistical assumptions. `nothing` means to make no statistical assumptions (use non-parametric methods) and `exact` means to assume measurements are exact (e.g., repeated measurement is not necessary to increase confidence). The default is `nothing`. In the future we could also support `normal`, but that's almost never the right assumption for benchmarks, so I'm omitting it for now.

Some concrete examples:

- The default units could be specified as `Unit ns/op lower=better assume=nothing`, `Unit MB/s higher=better assume=nothing`, etc. These would be built-in to the tooling.
- Various compiler benchmarking tools report the size of compiled binaries. This doesn't require repeated measurement, so these units could be specified like `Unit text-bytes lower=better assume=exact` or on the command-line as `-unit "text-bytes lower=better assume=exact"`.

/cc @rsc @mknyszek @dr2chase @jeremyfaller 