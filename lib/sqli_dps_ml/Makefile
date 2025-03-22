# Makefile for building the 'token' Python extension module

# Name of the final shared object
TARGET = token.so

# Source files
LEXFILE = lexer.l
LEX_C   = lex.yy.c
WRAPPER = wrapper.c

# Get Python include and ld flags using python3-config
PY_INCLUDES := $(shell python3-config --includes)
PY_LDFLAGS  := $(shell python3-config --ldflags)

# Compiler flags
CFLAGS = -fPIC $(PY_INCLUDES) -Wall -O2

# Linker flags for macOS Python extension bundles
LDFLAGS = -bundle -undefined dynamic_lookup $(PY_LDFLAGS)

all: $(TARGET)

# Generate lex.yy.c from the Flex file
$(LEX_C): $(LEXFILE)
	@echo "Running flex on $(LEXFILE)..."
	flex -o $(LEX_C) $(LEXFILE)

# Compile the generated lex.yy.c
lex.yy.o: $(LEX_C)
	@echo "Compiling $(LEX_C)..."
	gcc $(CFLAGS) -c $(LEX_C) -o lex.yy.o

# Compile the wrapper file
wrapper.o: $(WRAPPER) wrapper.h
	@echo "Compiling $(WRAPPER)..."
	gcc $(CFLAGS) -c $(WRAPPER) -o wrapper.o

# Link object files to create the shared module
$(TARGET): lex.yy.o wrapper.o
	@echo "Linking to create $(TARGET)..."
	gcc $(LDFLAGS) lex.yy.o wrapper.o -o $(TARGET)

clean:
	@echo "Cleaning up..."
	rm -f $(LEX_C) lex.yy.o wrapper.o 
