OBJS = GPIO_ON.o
ifdef DEBUG
DEBUGFLGS = -g
else
DEBUGFLGS =
endif

%.o : %.s
	as $(DEBUGFLGS) $< -o $@
GPIO_ON: $(OBJS)
	gcc -o GPIO_ON $(OBJS)

clean:
	rm *.o GPIO_ON
