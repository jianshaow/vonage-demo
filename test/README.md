# Test with api-simulator

~~~ shell
kubectl -nsimulator delete cm resp-body
kubectl -nsimulator create cm resp-body --from-file=ncco/
~~~
