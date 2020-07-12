pod() {
    selector=$1
    query='?(@.status.phase=="Running")'
    oc get pods --selector $selector -o jsonpath="{.items[$query].metadata.name}"
}

POD=$(pod name="blog")
echo $POD
