use std::collections::HashMap;

struct Structure<T> {
    pub data: T
}

impl<T> Structure<T> {
    pub fn new(data: T) -> Self {
        Self {data}
    }

    pub fn get(&self) -> &T {
        &self.data
    }

    pub fn get_mut(&mut self) -> &mut T {
        &mut self.data
    }
}

fn main() {
    println!("This is a macro");
    assert!(1 == 1);
    for i in 0..5 {
        println!("{}", i);
    }
}