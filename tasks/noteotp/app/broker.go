package main

import (
	"sync"
)

type Broker[T any] struct {
	subscribers map[chan<- T]struct{}
	sync.Mutex
}

func NewBroker[T any]() *Broker[T] {
	return &Broker[T]{
		subscribers: make(map[chan<- T]struct{}),
	}
}

func (b *Broker[T]) Subscribe(out chan<- T) (cancel func()) {
	b.Lock()
	defer b.Unlock()

	b.subscribers[out] = struct{}{}

	return func() {
		b.Lock()
		defer b.Unlock()
		delete(b.subscribers, out)
	}
}

func (b *Broker[T]) Publish(value T) {
	// NOTE We need force delivery order
	b.Lock()
	defer b.Unlock()

	toDelete := make([]chan<- T, 0)
	for ch := range b.subscribers {
		select {
		case ch <- value:
		default:
			toDelete = append(toDelete, ch)
		}
	}

	for _, ch := range toDelete {
		delete(b.subscribers, ch)
	}
}
