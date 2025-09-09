package pprof

import (
	"fmt"
	"io"
	"os"
	"path/filepath"
	"runtime"
	"runtime/pprof"
	"sync/atomic"

	"github.com/microsoft/typescript-go/internal/core"
)

var profileDir string
var heapProfileCounter int64

type profileSession struct {
	cpuFilePath string
	memFilePath string
	cpuFile     *os.File
	memFile     *os.File
	logWriter   io.Writer
}

// BeginProfiling starts CPU and memory profiling, writing the profiles to the specified directory.
func BeginProfiling(dir string, logWriter io.Writer) *profileSession {
	profileDir = dir
	if err := os.MkdirAll(profileDir, 0o755); err != nil {
		panic(err)
	}

	pid := os.Getpid()

	cpuProfilePath := filepath.Join(profileDir, fmt.Sprintf("%d-cpuprofile.pb.gz", pid))
	memProfilePath := filepath.Join(profileDir, fmt.Sprintf("%d-memprofile.pb.gz", pid))
	cpuFile, err := os.Create(cpuProfilePath)
	if err != nil {
		panic(err)
	}
	memFile, err := os.Create(memProfilePath)
	if err != nil {
		panic(err)
	}

	if err := pprof.StartCPUProfile(cpuFile); err != nil {
		panic(err)
	}

	return &profileSession{
		cpuFilePath: cpuProfilePath,
		memFilePath: memProfilePath,
		cpuFile:     cpuFile,
		memFile:     memFile,
		logWriter:   logWriter,
	}
}

func (p *profileSession) Stop() {
	pprof.StopCPUProfile()
	err := pprof.Lookup("allocs").WriteTo(p.memFile, 0)
	if err != nil {
		panic(err)
	}

	p.cpuFile.Close()
	p.memFile.Close()

	fmt.Fprintf(p.logWriter, "CPU profile: %v\n", p.cpuFilePath)
	fmt.Fprintf(p.logWriter, "Memory profile: %v\n", p.memFilePath)
}

func WriteHeapProfile(runGC bool) (string, error) {
	if profileDir == "" {
		profileDir = filepath.Join(core.Must(os.Getwd()), "pprof")
	}
	if err := os.MkdirAll(profileDir, 0o755); err != nil {
		return "", err
	}

	if runGC {
		runtime.GC()
		runtime.GC()
	}

	// Generate unique filename using PID and counter
	pid := os.Getpid()
	counter := atomic.AddInt64(&heapProfileCounter, 1)

	filename := fmt.Sprintf("%d-%d-heapprofile.pb.gz", pid, counter)
	filePath := filepath.Join(profileDir, filename)

	file, err := os.Create(filePath)
	if err != nil {
		return "", err
	}
	defer file.Close()

	err = pprof.Lookup("heap").WriteTo(file, 0)
	if err != nil {
		return "", err
	}

	return filePath, nil
}
