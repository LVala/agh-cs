#ifndef MYSTRING_H
#define MYSTRING_H

#include <set>
#include <map>
#include <vector>
#include <functional>

class MyString {
    public:
        static const size_t initialBufferSize = 20;
        static MyString generateRandomWord(size_t length);

        MyString() = default;
        MyString(const char *text);
        MyString(const MyString &text);

        size_t size() const {return _size;};
        bool empty() const {return _size == 0;};
        auto capacity() const {return initialBufferSize + text_dn.capacity();};
        void clear();
        MyString& trim();
        std::set<MyString> getUniqueWords() const;
        std::map<MyString,size_t> countWordsUsageIgnoringCases() const;
        MyString& toLower();
        bool startsWith(const char *text) const;
        bool endsWith(const char *text) const;
        MyString join(const std::vector<MyString> &texts) const;
        bool all_of(std::function<bool(char)> predicate) const;
        void push_back(char c);

        friend std::ostream& operator<< (std::ostream& stream, const MyString& text);
        friend std::istream& operator>> (std::istream& stream, MyString& text);
        bool operator==(const MyString& rhs) const;
        bool operator!=(const MyString& rhs) const;
        char& operator[] (size_t index);
        char operator[] (size_t index) const;
        MyString& operator+=(char rhc);
        bool operator< (const MyString& rhs) const;

        template<typename T>
        struct Iterator {
            typedef std::ptrdiff_t difference_type;
            typedef T value_type;
            typedef T* pointer;
            typedef T& reference;
            typedef std::forward_iterator_tag iterator_category;

            explicit Iterator(T* myString, size_t position) : _index(position),_string(myString) {}
            Iterator operator+(size_t pos){return Iterator(_string,_index+pos);}
            size_t operator-(Iterator other){return _index-other._index;};
            Iterator& operator++() {
                _index++;
                return *this;
            }
            Iterator& operator--() {
                _index--;
                return *this;
            }
            bool operator==(Iterator other){return _index==other._index && _string == other._string;}
            bool operator!=(Iterator other){return _index!=other._index || _string != other._string;}
            char operator*(){return (*_string)[_index];}

            T * _string;
            size_t _index;
        };

        typedef Iterator<MyString> iterator;
        typedef Iterator<const MyString> const_iterator;

        iterator begin() {return iterator(this, 0);};
        iterator end() {return iterator(this, _size);};
        const_iterator cbegin() {return const_iterator(this, 0);};
        const_iterator cend() {return const_iterator(this, _size);};
        const_iterator cbegin() const {return const_iterator(this, 0);};
        const_iterator cend() const {return const_iterator(this, _size);};


    private:
        char text_st[initialBufferSize+1] = {0};
        std::string text_dn = "";
        size_t _size = 0;
};


#endif