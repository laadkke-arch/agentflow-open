<!--
Our process for evaluating language changes can be found here:
https://go.googlesource.com/proposal/+/refs/heads/master#language-changes
-->

### Author background


- **Would you consider yourself a novice, intermediate, or experienced Go programmer?**
I consider myself as novice to intermediate Go programmer.  I have no extensive experience of looking at established Go code under the hood. 
- **What other languages do you have experience with?**
I have VB, C# and PHP experience before becoming interested in Go.

### Related proposals

- **Has this idea, or one like it, been proposed before?** 

  I'm not sure. I searched the proposals and I can't find a proposal that discussed the same.
 
- **Does this affect error handling?**. I'm not sure.

- **Is this about generics?** No.

### Proposal

- **What is the proposed change?**

I would like to suggest a language change that can execute dynamic assignments to a list of discrete variables.
I have the following code:

```go
 // Process options
if len(opts) == 1 {
  switch t := opts[0].(type) {
  case string:
	  if size64, err := strconv.ParseInt(t, 10, 32); err == nil {
		  size = int(size64)
	  }
  case int:
	  size = t
  default:
	  size = -1
  }
}

if len(opts) == 2 {
  switch t := opts[1].(type) {
  case string:
	  if size64, err := strconv.ParseInt(t, 10, 32); err == nil {
		  scale = uint8(size64)
	  }
  case int:
	  scale = uint8(t)
  case uint8:
	  scale = t
  default:
	  scale = 0
  }
}

if len(opts) == 3 {
  switch t := opts[2].(type) {
  case string:
	  if size64, err := strconv.ParseInt(t, 10, 32); err == nil {
		  prec = uint8(size64)
	  }
  case int:
	  prec = uint8(t)
  case uint8:
	  prec = t
  default:
	  scale = 0
  }
}
```

The ```opts``` variable is a variadic parameter in a function: 

```go
func NewExtParam(value interface{}, opts ...interface{}) ExtParam {
}
```
In order to check if one or more of the values have been set, I need to check the length of the ```opts``` variable in order to enter and process the value further. As you have noticed, there is no null checking yet.

It would be nice if we can destructure an array or a variadic variable like the one below:

```go
sz, sc, pr := opts...
```

And then we can write the following check if the value is null or not.

```go
if sz != nil {
  // process further
}
if sc!= nil {
  // process further
}
if pr != nil {
  // process further
}
```

- **Who does this proposal help, and why?** 

 It can help developers to simplify their code 

- **Please describe as precisely as possible the change to the language.**
- **What would change in the language spec?**
- **Please also describe the change informally, as in a class teaching Go.**

  The mechanics can be as follows:
   - It will only set the values specified in left-to-right order. Meaning, if there is no third (3) variable in the set, the assignment would not be prompted. A similar feature of this is the assertion operator or the map's second result.
  - A null value would be read if the destination is more than the length of the variadic or array input
 
- **Is this change backward compatible?**
  - Breaking the Go 1 compatibility guarantee is a large cost and requires a large benefit.
    Show example code before and after the change.
  - **Before**
  - **After**
- **Orthogonality: how does this change interact or overlap with existing features?**
- **Is the goal of this change a performance improvement?**
  - **If so, what quantifiable improvement should we expect?**
  - **How would we measure it?**

### Costs

- **Would this change make Go easier or harder to learn, and why?**

I think it will contribute to a more idiomatic Go concept. Instead of manually checking the length and indexing an array like the code I gave above, a quick and easy assignment like this would lessen the clutter. 

PHP has the ```list``` function. It made the values retrieval easy to code and understand.

- **What is the cost of this proposal? (Every language change has a cost).**
- **How many tools (such as vet, gopls, gofmt, goimports, etc.) would be affected?**
- **What is the compile time cost?**
- **What is the run time cost?**
- **Can you describe a possible implementation?**
- **Do you have a prototype? (This is not required.)**
