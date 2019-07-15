#include <iostream>
#include <iterator>
#include <vector>



// 假设数据分布在（0，100）之间，每个桶内部用链表表示，在数据入桶同时插入排序。然后把各个桶中的数据合并。


const int BUCKET_NUM = 10;

struct ListNode {
  explicit ListNode(int i = 0) : mData(i), mNext(NULL) {}
  ListNode* mNext;
  int mData;
};

ListNode* insert(ListNode *head, int val) {
  ListNode dummyNode;
  ListNode *newNode = new ListNode(val);
  ListNode *pre, *curr;
  dummyNode.mNext = head;
  pre = &dummyNode;
  curr = head;
  while (NULL != curr && curr->mData <= val) {
    pre = curr;
    curr = curr->mNext;
  }
  newNode->mNext = curr;
  pre->mNext = newNode;
  return dummyNode.mNext;
}

ListNode* Merge(ListNode *head1, ListNode *head2){
  ListNode dummyNode;
  ListNode *dummy = &dummyNode;
  while(NULL != head1 && NULL != head2){
    if(head1->mData <= head2->mData){
      dummy->mNext = head1;
      head1 = head1->mNext;
    }else{
      dummy->mNext = head2;
      head2 = head2->mNext;
    }
    dummy = dummy->mNext;
  }
  if (NULL != head1) dummy->mNext = head1;
  if (NULL != head2) dummy->mNext = head2;

  return dummyNode.mNext;
}

void BucketSort(int n,int arr[]){
  std::vector<ListNode*> buckets(BUCKET_NUM,(ListNode*)(0));
	for(int i=0;i<n;++i){
		int index = arr[i]/BUCKET_NUM;
		ListNode *head = buckets.at(index);
		buckets.at(index) = insert(head,arr[i]);
	}
	ListNode *head = buckets.at(0);
	for(int i=1;i<BUCKET_NUM;++i){
		head = Merge(head,buckets.at(i));
	}
	for(int i=0;i<n;++i){
		arr[i] = head->mData;
		head = head->mNext;
	}
}