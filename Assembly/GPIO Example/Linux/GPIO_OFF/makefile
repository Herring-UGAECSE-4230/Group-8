OBJS = GPIO_OFF.o
ifdef DEBUG
DEBUGFLGS = -g
else
DEBUGFLGS =
endif

%.o : %.s
	as $(DEBUGFLGS) $< -o $@
GPIO_OFF: $(OBJS)
	gcc -o GPIO_OFF $(OBJS)

clean:
	rm *.o GPIO_OFF
