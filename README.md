# Data Collection using AWS Mechanical Turk

A demo for how to use mechanical turk to create tasks and collect data. 


## Steps

- Create a requester account in https://requester.mtruk.com
- Create a new project and choose **Data Collection** template
- Specify properties and design layout
- Publish batches

## Things to consider while specifying properties

- **Reward per assignment:** Cost per task per worker
- **Number of assignments per task:** Number of respondents for the same data ( can be used for verification )
- **Time alloted per assignment**
- **Task expires in:** The time by when we need the data
- **Auto approve and pay workers in:** The time we require to verify the answers


## Qualification type

The qualification type is used to evaluate the workers whether they are fit to answer our survey. A simple qualification type is a qualification test. Simply, we can post few of the questions of our original task and test them against an answer key. 

**Note**: 
- The questions should be of multiple choice in order to automatically verify using a key. Hence, we cannot have text questions in this qualification test.
- The style attribute cannot be used in a image ( So we need to use a image of proper dimensions ).

In addition to this, we can also have some basic qualifications like the approval rate should be greater than 50% etc. 

## Reference

https://blog.mturk.com/
