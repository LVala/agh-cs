module Demo {
  interface FUWSObject {
    // Frequently Used, With State Object
    // for instance something like Singleton
    // this object is very frequently used and allows for
    // some type of state and/or caching
    // so it makes sense to implement it as a one-to-one servant in ASM
    int incrementAndGet();
  };

  interface RUWSObject {
    // Rarely Used, With State Object
    // this object is rarely used, so needs to be created
    // only when there's need
    // but when it is created, it contains some state that should not
    // be shared for some reason, so it is not implemented as a default
    // servant, which would have to use mutex, for instance, when accessing 
    // the shared state, as its methods can be run by multiple threads
    // with servant locator, which creates new servant for every call,
    // its not needed
    void saveALotOfData(string data);
  };

  interface FUWOSObject {
    // Frequently Used, Without State Object
    // this object can be implementd with default servant
    // as it doesn't suffer from aforementioned issues
    // and thanks to that, can scale nicely
    idempotent string concatWords(string first, string second);
  };
};
