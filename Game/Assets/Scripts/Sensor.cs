using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.InputSystem;
using UnityEngine.UI;
public class Sensor : MonoBehaviour
{

    public GameObject Lightning;

    // private GameObject[] lightnings;
    private GameObject[] enemies;
    bool isLightningOn;
    float accelerometerUpdateInterval = 1.0f / 60.0f;
    float lowPassKernelWidthInSeconds = 1.0f;
    float shakeDetectionThreshold = 2.0f;
    float lowPassFilterFactor;
    Vector3 lowPassValue;


    private Vector3 getAcceleration(){
        return Accelerometer.current.acceleration.ReadValue();
    }

    // Start is called before the first frame update
    void Start()
    {
        isLightningOn = false;
        InputSystem.EnableDevice(Accelerometer.current);
        lowPassFilterFactor = accelerometerUpdateInterval / lowPassKernelWidthInSeconds;
        shakeDetectionThreshold *= shakeDetectionThreshold;
        lowPassValue = getAcceleration();

    }

     IEnumerator Reset(float Count){
        yield return new WaitForSeconds(Count);
        isLightningOn = false;
        yield return null;
    }

    public void activateLightningIn(float Count){
         StartCoroutine("Reset", Count);
    }
    private void launchThunder(){

        if(!isLightningOn){
            isLightningOn = true;

            foreach (GameObject enemy in enemies){
                Vector3 enemyPosition = enemy.transform.position;
                GameObject clone = Instantiate(Lightning, enemyPosition, Quaternion.identity);
                Destroy(clone, 1);
                Destroy(enemy);
            }
             StartCoroutine("Reset", 5);
        }
    }

  
    // Update is called once per frame
    void Update()
    {
        enemies = GameObject.FindGameObjectsWithTag("Enemy");
        Vector3 acceleration = getAcceleration();
        lowPassValue = Vector3.Lerp(lowPassValue, acceleration, lowPassFilterFactor);
        Vector3 deltaAcceleration = acceleration - lowPassValue;

        if (deltaAcceleration.sqrMagnitude >= shakeDetectionThreshold)
        {
            launchThunder();
        }

    }   

    void onDestroy(){
        InputSystem.DisableDevice(Accelerometer.current);
    }

}
