package docker

import "io"

type BuildOptions struct {
	Context            io.Reader
	Dockerfile         string
	Remove             bool
	BuildArgs          map[string]*string
	Target             string
	SSHSpecs           []string
	SecretSpecs        []string
	Network            string
	CacheFrom          []string
	PullParent         bool
	Platform           string
	ExtraTags          []string
	ForceLegacyBuilder bool
}
